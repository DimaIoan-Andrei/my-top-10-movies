# My Top 10 Movies

This is a personal movie ranking web application built using Flask. It allows you to maintain your own curated list of top movies, assign personal ratings, write short reviews, and visually display each movie using a card-flip interface. Movies can be added directly from The Movie Database (TMDb) API through title search.

## Features

- Display and rank your favorite movies.
- Add movies using TMDb API search.
- Select from a list of matching results before adding.
- Edit the rating and review of a movie at any time.
- Delete movies from the ranking list.
- Data is stored in an SQLite database managed through SQLAlchemy ORM.

## Technologies Used

- Python 3
- Flask
- SQLAlchemy / Flask-SQLAlchemy
- Flask-WTF and WTForms
- Bootstrap-Flask
- Requests (for TMDb API interaction)
- SQLite (local persistent storage)

## Project Structure

my-top-10-movies/
│ app.py
│ requirements.txt
│ .env # contains TMDB_API_KEY (not included in repository)
│ .gitignore
│ README.md
│
├─ instance/ # contains movies.db (ignored by Git)
│
├─ templates/ # HTML templates
│
└─ static/ # CSS and other static files

## Setup Instructions

1. Clone the repository:
git clone https://github.com/DimaIoan-Andrei/my-top-10-movies.git

cd my-top-10-movies

2. Create and activate a virtual environment:
python -m venv .venv
.venv\Scripts\activate # Windows

3. Install dependencies:
pip install -r requirements.txt

4. Create a `.env` file in the project directory and add your TMDb API Key:
TMDB_API_KEY=your_api_key_here

5. Run the application:
python app.py

6. View the application in your browser:
http://localhost:5000

## Database

The application uses SQLite for persistent storage.  
The database file is automatically created inside the `instance/` directory on first run.

## Notes

- The `.env` file and the database directory are excluded from version control.
- This project is designed for local use and portfolio presentation, not public multi-user access.

## License

This project is shared for personal and educational use. You may modify and extend it as needed.
