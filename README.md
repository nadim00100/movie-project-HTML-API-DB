# 🎬 Movie Database CLI & Website Generator

A Python project that lets you manage a personal movie database through a command-line interface (CLI) and generate a website to showcase your collection.

## 📌 Features

- Add movies by title (automatically fetches info from the OMDb API)
- List all stored movies
- Delete or update movies
- Search and filter movies
- Show random movie pick
- Display movie statistics (average, median, best, worst)
- Sort movies by rating or release year
- Generate a stylish HTML website with poster images

## 🛠️ Tech Stack

- Python 3
- SQLite (via SQLAlchemy)
- OMDb API (for fetching movie data)
- HTML & CSS (for website generation)

## 📂 Project Structure

movie-project/
│
├── main.py
├── movies.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── /data/
│   └── movies.db
│
├── /static/
│   ├── index_template.html
│   ├── index.html
│   └── style.css
│
├── /storage/
│   ├── __init__.py
│   └── movie_storage_sql.py


## 🚀 Setup

#1. Clone the repository
```bash

git clone https://github.com/nadim00100/movie-project-HTML-API-DB.git
cd movie-project

#2. Create and activate a virtual environment (recommended)
```bash

python -m venv venv  
source venv/bin/activate  # Linux/macOS  
venv\Scripts\activate     # Windows 
 
#3. Install dependencies
```bash

pip install -r requirements.txt 
 
#4. Create a .env file in the project root with your configuration:
```ini

OMDB_API_KEY=your_omdb_api_key_here  
DB_URL=sqlite:///data/movies.db
  
5. Run the application
```bash

python movies.py


📖 Usage
Follow the on-screen menu to add, list, update, delete, and search movies.

Use the "Generate website" option to create a static HTML page showcasing your movie collection with posters.

The database is stored in data/movies.db by default.

🔗 External Resources
OMDb API — For fetching movie information

SQLAlchemy — Database ORM

Python dotenv — To manage environment variables


© 2025 Nadim almasri

