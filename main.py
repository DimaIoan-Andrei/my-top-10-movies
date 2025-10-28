from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)

class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(500), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=True)

with app.app_context():
    db.create_all()

class EditForm(FlaskForm):
    rating = FloatField("Your Rating out of 10 e.g. 7.5", validators=[DataRequired()])
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Done")

class AddMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")

@app.route("/")
def home():
    movies = Movie.query.order_by(Movie.rating.desc()).all()
    for idx, movie in enumerate(movies, start=1):
        movie.ranking = idx
    db.session.commit()

    return render_template('index.html', movies=movies)

@app.route("/edit/<int:movie_id>", methods=["GET", "POST"])
def edit(movie_id):
    form = EditForm()
    movie = db.session.get(Movie, movie_id)

    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))

    form.rating.data = movie.rating
    form.review.data = movie.review

    return render_template("edit.html", form=form, movie=movie)

@app.route("/delete/<int:movie_id>", methods=["GET", "POST"])
def delete_movie(movie_id):
    movie = db.session.get(Movie, movie_id)
    if movie:
        db.session.delete(movie)
        db.session.commit()
    return redirect(url_for("home"))

@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = AddMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(
            "https://api.themoviedb.org/3/search/movie",
            params={
                "api_key": TMDB_API_KEY,
                "query": movie_title,
            }
        )
        data = response.json()["results"]
        return render_template("select.html", movies=data)
    return render_template("add.html", form=form)

@app.route("/find/<int:movie_id>")
def find_movie(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}",
        params={"api_key": TMDB_API_KEY, "language": "en-US"}
    )
    data = response.json()

    new_movie = Movie(
        title=data["title"],
        year=int(data["release_date"][:4]) if data.get("release_date") else None,
        description=data["overview"],
        img_url=f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    )

    db.session.add(new_movie)
    db.session.commit()

    return redirect(url_for("edit", movie_id=new_movie.id))


if __name__ == '__main__':
    app.run(debug=True)
