
from flask import Flask, request, jsonify
import pandas as pd
from models import db, Movie,MovieLanguage
from config import Config
from datetime import datetime
import concurrent.futures

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Used To avoid using flask migration commands everytime code model changes
with app.app_context():
    db.create_all() 

def process_batch(batch):
    with app.app_context(): 
        for row in batch:
            try:

                movie = Movie(
                    title=row['title'],
                    original_title=row['original_title'],
                    release_date=datetime.strptime(row['release_date'], '%Y-%m-%d').date() if pd.notna(row['release_date']) else None,
                    original_language=row['original_language'],
                    budget=float(row['budget']) if pd.notna(row['budget']) else 0.0,
                    revenue=float(row['revenue']) if pd.notna(row['revenue']) else 0.0,
                    runtime=float(row['runtime']) if pd.notna(row['runtime']) else 0.0,
                    vote_average=float(row['vote_average']) if pd.notna(row['vote_average']) else 0.0,
                    vote_count=int(row['vote_count']) if pd.notna(row['vote_count']) else 0,
                    overview=row['overview'],
                    genre_id=int(row['genre_id']) if pd.notna(row['genre_id']) else None,
                    production_company_id=int(row['production_company_id']) if pd.notna(row['production_company_id']) else None,
                    homepage=row['homepage']
                )

                db.session.add(movie)

                db.session.commit()

                languages_list = eval(row['languages']) if pd.notna(row['languages']) else []

                for language in languages_list:

                    movie_language = MovieLanguage(language=language, movie_id=movie.id)
                    db.session.add(movie_language)

                
                db.session.commit()
                print(f"Processed and saved movie: {movie.title}")

            except Exception as e:
                db.session.rollback()
                print(f"Error processing row: {row}. Exception: {str(e)}")

@app.route('/upload', methods=['POST'])
def upload_csv():

    if 'file' not in request.files:

        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':

        return jsonify({"error": "No selected file"}), 400
    
    if file and file.filename.endswith('.csv'):

        df = pd.read_csv(file)
        total_rows = len(df)
        chunk_size = total_rows // 10
        batches = [df.iloc[i:i + chunk_size] for i in range(0, total_rows, chunk_size)]

        # Processing each batch concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(process_batch, batch.to_dict(orient='records')) for batch in batches]

            # Wait for all threads to complete
            for future in concurrent.futures.as_completed(futures):
                future.result()  # Retrieve the result to throw error, if any threads fails abruptly

        return jsonify({"message": "File uploaded and processed successfully"}), 201
    
    return jsonify({"error": "Invalid file format"}), 400



@app.route('/movies', methods=['GET'])
def get_movies():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    language = request.args.get('language')
    year_of_release = request.args.get('year_of_release', type=int)
    sort_by = request.args.get('sort_by', 'release_date')
    order = request.args.get('order', 'asc')

    query = Movie.query

    # Filtering by language from the MovieLanguage table by joining movie_lang table
    if language:
        query = query.join(Movie.languages).filter(MovieLanguage.language == language)

    # Filtering by year of release
    if year_of_release:
        query = query.filter(db.extract('year', Movie.release_date) == year_of_release)

    # Sorting by release date or any specified field
    if hasattr(Movie, sort_by):  
        if order == 'desc':
            query = query.order_by(getattr(Movie, sort_by).desc())
        else:
            query = query.order_by(getattr(Movie, sort_by).asc())
    else:
        return jsonify({"error": "Invalid sort field"}), 400


    movies = query.paginate(page=page, per_page=per_page)

    data = [{
        'title': movie.title,
        'original_title': movie.original_title,
        'release_date': movie.release_date.isoformat() if movie.release_date else None,
        'original_language': movie.original_language,
        'budget': movie.budget,
        'revenue': movie.revenue,
        'runtime': movie.runtime,
        'vote_average': movie.vote_average,
        'vote_count': movie.vote_count,
        'overview': movie.overview,
        'genre_id': movie.genre_id,
        'production_company_id': movie.production_company_id,
        'homepage': movie.homepage,
        'languages': [lang.language for lang in movie.languages]
    } for movie in movies.items]

    return jsonify({
        'movies': data,
        'total': movies.total,
        'pages': movies.pages,
        'current_page': movies.page,
        'has_next': movies.has_next
    })

if __name__ == '__main__':
    app.run(debug=True)


