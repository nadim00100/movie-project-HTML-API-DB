# movies.py

import random
import statistics
import requests
import os
from dotenv import load_dotenv
import movie_storage_sql as storage

# Load environment variables
load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
OMDB_URL = "http://www.omdbapi.com/"

def press_enter():
    """Pause the program until the user presses Enter."""
    input("\nPress Enter to continue...")

def movies_list():
    """Print the list of movies in the database."""
    movies = storage.list_movies()
    if not movies:
        print("No movies in the database.")
    else:
        print(f"\n{len(movies)} movies in total:")
        for title, info in movies.items():
            print(f"{title} ({info['year']}): {info['rating']}")

def add_movie():
    """Add a new movie by fetching from OMDb API."""
    title_input = input("Enter movie title: ").strip()
    if not title_input:
        print("Title must not be empty.")
        return

    params = {"t": title_input, "apikey": OMDB_API_KEY}
    try:
        response = requests.get(OMDB_URL, params=params, timeout=5)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("⚠️ Error: Unable to connect to the OMDb API. Please check your internet connection.")
        return
    except requests.exceptions.HTTPError as e:
        print(f"⚠️ HTTP error occurred: {e}")
        return
    except requests.exceptions.RequestException as e:
        print(f"⚠️ An unexpected error occurred: {e}")
        return

    data = response.json()
    if data.get("Response") != "True":
        print(f"❌ Movie not found in OMDb: {data.get('Error', 'Unknown error')}")
        return

    try:
        movie_title = data["Title"]
        year = int(data["Year"].split("–")[0])
        imdb_rating = data.get("imdbRating", "N/A")
        rating = float(imdb_rating) if imdb_rating != "N/A" else 0.0
        poster_url = data.get("Poster", "N/A")
    except (KeyError, ValueError):
        print("❌ Unexpected data format from OMDb. Could not parse movie info.")
        return

    movies = storage.list_movies()
    if movie_title in movies:
        print("This movie already exists.")
        return

    try:
        storage.add_movie(movie_title, year, rating, poster_url)
        print(f"✅ Added: {movie_title} ({year}), rating: {rating}")
        if poster_url and poster_url != "N/A":
            print(f"📷 Poster URL: {poster_url}")
    except Exception as e:
        print(f"❌ Failed to save movie to the database: {e}")

def delete_movie():
    """Delete a movie from the database by name."""
    name = input("Enter movie name to delete: ").strip()
    if not name:
        print("No empty input allowed.")
        return

    movies = storage.list_movies()
    # Find title matching case-insensitive
    matched_title = None
    for title in movies:
        if title.lower() == name.lower():
            matched_title = title
            break

    if matched_title:
        try:
            storage.delete_movie(matched_title)
            print(f"Movie '{matched_title}' successfully deleted.")
        except Exception as e:
            print(f"Failed to delete movie: {e}")
    else:
        print("Movie not found.")

def update_movie():
    """Update the rating of an existing movie."""
    name = input("Enter movie name to update: ").strip()
    if not name:
        print("No empty input allowed.")
        return

    movies = storage.list_movies()
    matched_title = None
    for title in movies:
        if title.lower() == name.lower():
            matched_title = title
            break

    if not matched_title:
        print("Movie not found.")
        return

    while True:
        rating_input = input("Enter new rating (0-10): ").strip()
        try:
            rating = float(rating_input)
            if 0 <= rating <= 10:
                try:
                    storage.update_movie(matched_title, rating)
                    print(f"Movie '{matched_title}' successfully updated.")
                    return
                except Exception as e:
                    print(f"Failed to update movie: {e}")
                    return
            else:
                print("Rating must be between 0.0 and 10.0.")
        except ValueError:
            print("Invalid rating.")

def movie_stats():
    """Display statistics about the movies in the database."""
    movies = storage.list_movies()
    if not movies:
        print("No movies in the database.")
        return
    ratings = [info['rating'] for info in movies.values()]
    avg = sum(ratings) / len(ratings)
    med = statistics.median(ratings)
    max_rating = max(ratings)
    min_rating = min(ratings)
    best = [title for title, info in movies.items() if info['rating'] == max_rating]
    worst = [title for title, info in movies.items() if info['rating'] == min_rating]
    print(f"\nAverage rating: {avg:.1f}")
    print(f"Median rating: {med:.1f}")
    print(f"Best movie(s) ({max_rating}): {', '.join(best)}")
    print(f"Worst movie(s) ({min_rating}): {', '.join(worst)}")

def random_movie():
    """Pick and display a random movie from the database."""
    movies = storage.list_movies()
    if not movies:
        print("No movies in the database.")
        return
    title, info = random.choice(list(movies.items()))
    print(f"\nYour movie for tonight: {title} ({info['year']}), rated {info['rating']}")

def search_movie():
    """Search for movies by name substring."""
    movies = storage.list_movies()
    query = input("Enter part of movie name: ").strip().lower()
    if not query:
        print("No empty input allowed.")
        return
    found = False
    for title, info in movies.items():
        if query in title.lower():
            print(f"{title} ({info['year']}): {info['rating']}")
            found = True
    if not found:
        print("Movie not found.")

def sort_movies_by_rating():
    """Sort and display movies by rating in descending order."""
    movies = storage.list_movies()
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['rating'], reverse=True)
    for title, info in sorted_movies:
        print(f"{title} ({info['year']}): {info['rating']}")

def sort_movies_by_year():
    """Sort and display movies by year, ascending or descending."""
    movies = storage.list_movies()
    order = input("Do you want the latest movies first? (Y/N): ").strip().lower()
    reverse = order == 'y'
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['year'], reverse=reverse)
    for title, info in sorted_movies:
        print(f"{title} ({info['year']}): {info['rating']}")

def filter_movies():
    """Filter movies by minimum rating and/or year range."""
    movies = storage.list_movies()

    # Get validated minimum rating or None
    while True:
        min_rating_input = input("Enter minimum rating (0-10, leave blank for no minimum): ").strip()
        if not min_rating_input:
            min_rating = None
            break
        try:
            min_rating = float(min_rating_input)
            if 0 <= min_rating <= 10:
                break
            else:
                print("Rating must be between 0 and 10.")
        except ValueError:
            print("Invalid rating. Please enter a number between 0 and 10.")

    # Get start and end years or None
    def parse_year(s):
        try:
            return int(s)
        except ValueError:
            return None

    start_year_input = input("Enter start year (leave blank for no start): ").strip()
    start_year = parse_year(start_year_input) if start_year_input else None

    end_year_input = input("Enter end year (leave blank for no end): ").strip()
    end_year = parse_year(end_year_input) if end_year_input else None

    def is_valid(info):
        if min_rating is not None and info['rating'] < min_rating:
            return False
        if start_year is not None and info['year'] < start_year:
            return False
        if end_year is not None and info['year'] > end_year:
            return False
        return True

    filtered = False
    for title, info in movies.items():
        if is_valid(info):
            print(f"{title} ({info['year']}): {info['rating']}")
            filtered = True
    if not filtered:
        print("No movies match the filter criteria.")

def generate_website():
    """Generate a static HTML website from the template and movie data."""
    template_path = os.path.join("static", "index_template.html")
    output_path = os.path.join("static", "index.html")

    # Load template
    try:
        with open(template_path, "r", encoding="utf-8") as file:
            template = file.read()
    except FileNotFoundError:
        print("❌ Template file not found.")
        return

    # Set the page title
    page_title = "My Movie Collection"

    # Create the movie grid HTML
    movies = storage.list_movies()
    grid_items = ""
    for title, info in movies.items():
        grid_items += f"""
        <li>
            <div class="movie">
                <img class="movie-poster" src="{info['poster_url']}" alt="{title} poster">
                <div class="movie-title">{title}</div>
                <div class="movie-year">{info['year']} | ⭐ {info['rating']}</div>
            </div>
        </li>
        """

    movie_grid = f"""
    
    <ul class="movie-grid">
        {grid_items}
    </ul>
    """

    # Replace placeholders in template
    output = template.replace("__TEMPLATE_TITLE__", page_title).replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

    # Save to output file
    try:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(output)
        print("Website was generated successfully.")
    except Exception as e:
        print(f"❌ Failed to generate website: {e}")


def main():
    """Main function to run the movie database CLI."""
    options = {
        '1': movies_list,
        '2': add_movie,
        '3': delete_movie,
        '4': update_movie,
        '5': movie_stats,
        '6': random_movie,
        '7': search_movie,
        '8': sort_movies_by_rating,
        '9': sort_movies_by_year,
        '10': filter_movies,
        '11': generate_website  # ← added here
    }

    print("\n********** My Movies Database **********")
    while True:
        print(""" Menu:
        0. Exit
        1. List movies
        2. Add movie
        3. Delete movie
        4. Update movie
        5. Stats
        6. Random movie
        7. Search movie
        8. Movies sorted by rating
        9. Movies sorted by year
        10. Filter movies
        11. Generate website
        """)

        choice = input("Enter choice (0-10): ").strip()

        if choice == '0':
            print("Bye! See you later.")
            break

        action = options.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")

        press_enter()

if __name__ == "__main__":
    main()
