# main.py

import movies as m

def main():
    """Main function to run the movie database CLI."""
    options = {
        '1': m.movies_list,
        '2': m.add_movie,
        '3': m.delete_movie,
        '4': m.update_movie,
        '5': m.movie_stats,
        '6': m.random_movie,
        '7': m.search_movie,
        '8': m.sort_movies_by_rating,
        '9': m.sort_movies_by_year,
        '10': m.filter_movies,
        '11': m.generate_website
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

        choice = input("Enter choice (0-11): ").strip()

        if choice == '0':
            print("Bye! See you later.")
            break

        action = options.get(choice)
        if action:
            action()
        else:
            print("Invalid choice.")

        m.press_enter()

if __name__ == "__main__":
    main()
