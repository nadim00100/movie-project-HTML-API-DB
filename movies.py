import random
import statistics
from datetime import datetime
import movie_storage_sql as storage


def press_enter():
    """Wait for the user to press Enter before continuing."""
    input("\nPress Enter to continue...")


def movies_list():
    """Display all movies in the database with their year and rating."""
    movies = storage.list_movies()
    if not movies:
        print("No movies in the database.")
    else:
        print(f"\n{len(movies)} movies in total:")
        for title, info in movies.items():
            print(f"{title} ({info['year']}): {info['rating']}")


def add_movie():
    """
    Prompt the user to add a new movie to the database.

    Validates that the name is unique, the year is valid, and the rating is between 0.0 and 10.0.
    """
    movies = storage.list_movies()

    while True:
        name = input("Enter new movie name: ").strip()
        if not name:
            print("Movie name must not be empty.")
            continue
        if name in movies:
            print("This movie already exists.")
            return
        break

    current_year = datetime.now().year
    while True:
        try:
            year = int(input("Enter movie year: "))
            if 1888 <= year <= current_year:
                break
            print(f"Year must be between 1888 and {current_year}.")
        except ValueError:
            print("Invalid year.")

    while True:
        try:
            rating = float(input("Enter movie rating (0-10): "))
            if 0 <= rating <= 10:
                break
            print("Rating must be between 0.0 and 10.0.")
        except ValueError:
            print("Invalid rating.")

    storage.add_movie(name, year, rating)


def delete_movie():
    """
    Prompt the user to delete a movie by name.

    Searches for the movie by title (case-insensitive) and deletes it if found.
    """
    name = input("Enter movie name to delete: ").strip()
    if not name:
        print("No empty input allowed.")
        return

    movies = storage.list_movies()
    for title in movies:
        if title.lower() == name.lower():
            storage.delete_movie(title)
            return
    print("Movie not found.")


def update_movie():
    """
    Prompt the user to update a movie's rating.

    Validates the new rating before applying the update.
    """
    name = input("Enter movie name to update: ").strip()
    movies = storage.list_movies()
    for title in movies:
        if title.lower() == name.lower():
            while True:
                try:
                    rating = float(input("Enter new rating (0-10): "))
                    if 0 <= rating <= 10:
                        storage.update_movie(title, rating)
                        return
                    print("Rating must be between 0.0 and 10.0.")
                except ValueError:
                    print("Invalid rating.")
            return
    print("Movie not found.")


def movie_stats():
    """
    Display statistics for all movies in the database.

    Shows average rating, median rating, best and worst rated movies.
    """
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
    """Select and display a random movie from the database."""
    movies = storage.list_movies()
    if not movies:
        print("No movies in the database.")
        return
    title, info = random.choice(list(movies.items()))
    print(f"\nYour movie for tonight: {title} ({info['year']}), rated {info['rating']}")


def search_movie():
    """Search and display movies that match a substring of the title."""
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
    """Sort and display movies by year in ascending or descending order."""
    movies = storage.list_movies()
    order = input("Do you want the latest movies first? (Y/N): ").strip().lower()
    reverse = order == 'y'
    sorted_movies = sorted(movies.items(), key=lambda x: x[1]['year'], reverse=reverse)
    for title, info in sorted_movies:
        print(f"{title} ({info['year']}): {info['rating']}")


def filter_movies():
    """
    Filter and display movies by minimum rating and/or year range.

    Prompts the user for optional minimum rating, start year, and end year.
    """
    movies = storage.list_movies()
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

    start_year_input = input("Enter start year (leave blank for no start): ").strip()
    end_year_input = input("Enter end year (leave blank for no end): ").strip()

    def is_valid(info):
        rating_value = info['rating']
        year_value = info['year']
        if min_rating_input:
            try:
                if rating_value < float(min_rating_input):
                    return False
            except ValueError:
                pass
        if start_year_input:
            try:
                if year_value < int(start_year_input):
                    return False
            except ValueError:
                pass
        if end_year_input:
            try:
                if year_value > int(end_year_input):
                    return False
            except ValueError:
                pass
        return True

    for title, info in movies.items():
        if is_valid(info):
            print(f"{title} ({info['year']}): {info['rating']}")


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
        '10': filter_movies
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
