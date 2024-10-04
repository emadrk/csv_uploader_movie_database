# CSV Uploader Movie Database

This project allows users to upload movie data via a CSV file and query the data using specific filters such as language, year of release, and sorting options.

## Table of Contents
1. [Setting up the Environment](#setting-up-the-environment)
2. [Activating the Virtual Environment](#activating-the-virtual-environment)
3. [Running the Application](#running-the-application)
4. [Upload Movie Data (CSV)](#upload-movie-data)
5. [Query Movies](#query-movies)

## Setting up the Environment

1. **Clone the repository:**
   ```bash
   git clone https://github.com/emadrk/csv_uploader_movie_database.git
   cd csv_uploader_movie_database
   ```

2. **Creation and Activation of virtual environment:**
   ```
   python3 -m venv venv
   ```

   ```
   source venv/bin/activate

   ```

    ```
   pip install -r dependency.txt

   ```

3. **Running the Application:**
   ```
   python3 app.py
   ```

4. **Upload movie data:**
   ```
   curl --location 'http://127.0.0.1:5000/upload' \
    --form 'file=@"/path/to/your/movies_data_assignment.csv"'
   ```  

5. **Query movies:**
   ```
   http://127.0.0.1:5000/movies?language=&year_of_release=2014&sort_by=release_date=&order=desc&page=1&per_page=10
   ```

