from sqlalchemy import create_engine, text

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=False)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL
        )
    """))
    connection.commit()


def list_movies():
    """
    Retrieve all movies from the database.

    Returns:
        dict: A dictionary where the keys are movie titles and values
        are dictionaries containing 'year' and 'rating'.
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT title, year, rating FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"year": row[1], "rating": row[2]} for row in movies}


def add_movie(title, year, rating):
    """
    Add a new movie to the database.

    Args:
        title (str): The title of the movie.
        year (int): The release year of the movie.
        rating (float): The rating of the movie.
    """
    with engine.connect() as connection:
        try:
            connection.execute(
                text("INSERT INTO movies (title, year, rating) VALUES (:title, :year, :rating)"),
                {"title": title, "year": year, "rating": rating}
            )
            connection.commit()
            print(f"Movie '{title}' added successfully.")
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """
    Delete a movie from the database by title.

    Args:
        title (str): The title of the movie to delete.
    """
    with engine.connect() as connection:
        try:
            result = connection.execute(
                text("DELETE FROM movies WHERE title = :title"),
                {"title": title}
            )
            connection.commit()
            if result.rowcount:
                print(f"Movie '{title}' deleted successfully.")
            else:
                print(f"Movie '{title}' not found.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(title, rating):
    """
    Update the rating of a specific movie.

    Args:
        title (str): The title of the movie to update.
        rating (float): The new rating value.
    """
    with engine.connect() as connection:
        try:
            result = connection.execute(
                text("UPDATE movies SET rating = :rating WHERE title = :title"),
                {"title": title, "rating": rating}
            )
            connection.commit()
            if result.rowcount:
                print(f"Movie '{title}' updated successfully.")
            else:
                print(f"Movie '{title}' not found.")
        except Exception as e:
            print(f"Error: {e}")
