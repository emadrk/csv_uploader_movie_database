from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class MovieLanguage(db.Model):
    __tablename__ = 'movie_lang'

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    language = db.Column(db.String(100), nullable=False)

    movie = db.relationship('Movie', back_populates='languages')

class Movie(db.Model):
    __tablename__ = 'movie'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=True)
    original_title = db.Column(db.Text, nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    original_language = db.Column(db.Text, nullable=True)
    budget = db.Column(db.Text, nullable=True)
    revenue = db.Column(db.Text, nullable=True)
    runtime = db.Column(db.Text, nullable=True)
    vote_average = db.Column(db.Text, nullable=True)
    vote_count = db.Column(db.Text, nullable=True)
    overview = db.Column(db.Text, nullable=True)
    genre_id = db.Column(db.Text, nullable=True)
    production_company_id = db.Column(db.Text, nullable=True)
    homepage = db.Column(db.Text, nullable=True)

    languages = db.relationship('MovieLanguage', back_populates='movie', cascade='all, delete-orphan')