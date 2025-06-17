# movie_storage_sql.py

"""
Movie storage module with plain functions, using SQLAlchemy.
Loads DB_URL from .env automatically.
"""

from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text

# Load .env environment variables
load_dotenv()

DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise ValueError("DB_URL is not set in the .env file")

engine = create_engine(DB_URL, echo=False)

# Create the movies table if it doesn't exist
with engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT
        )
    """))
    conn.commit()

def list_movies():
    """
    Return all movies as a dict: title -> {year, rating, poster_url}
    """
    with engine.connect() as conn:
        result = conn.execute(text("SELECT title, year, rating, poster_url FROM movies"))
        movies = result.fetchall()
    return {row[0]: {"year": row[1], "rating": row[2], "poster_url": row[3]} for row in movies}

def add_movie(title, year, rating, poster_url=None):
    """
    Add a new movie to the database.
    """
    with engine.connect() as conn:
        try:
            conn.execute(
                text("INSERT INTO movies (title, year, rating, poster_url) VALUES (:title, :year, :rating, :poster_url)"),
                {"title": title, "year": year, "rating": rating, "poster_url": poster_url}
            )
            conn.commit()
        except Exception as e:
            raise RuntimeError(f"Failed to add movie: {e}")

def delete_movie(title):
    """
    Delete a movie by title.
    """
    with engine.connect() as conn:
        result = conn.execute(text("DELETE FROM movies WHERE title = :title"), {"title": title})
        conn.commit()
        if result.rowcount == 0:
            raise RuntimeError(f"Movie '{title}' not found")

def update_movie(title, rating):
    """
    Update the rating of a movie by title.
    """
    with engine.connect() as conn:
        result = conn.execute(text("UPDATE movies SET rating = :rating WHERE title = :title"), {"rating": rating, "title": title})
        conn.commit()
        if result.rowcount == 0:
            raise RuntimeError(f"Movie '{title}' not found")