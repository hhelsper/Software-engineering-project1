"""This is the file that houses the main driver code for my web app"""
import os
from tmdb_api_call import get_movie_data
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    current_user,
    logout_user,
)
from flask import Flask, render_template, request, Blueprint, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import find_dotenv, load_dotenv


app = Flask(__name__)

app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

load_dotenv(find_dotenv())
# Point SQLAlchemy to your Heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.login_view = "hello_world"
login_manager.init_app(app)

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    """This is the User Model"""

    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        """Neccessary function for Flask Login"""
        return "<User %r" % self.user_name

    def get_username(self):
        """Neccessary function for Flask Login"""
        return self.user_name

    def get_id(self):
        """Neccessary function for Flask Login"""
        return self.user_id


@login_manager.user_loader
def load_user(user_id):
    """Neccessary function for Flask Login"""
    return User.query.get(int(user_id))


class Rating(db.Model):
    """This is the Ratings model"""

    __tablename__ = "rating"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    movie_name = db.Column(db.String(120), nullable=False)


class Comment(db.Model):
    """This is the comments model"""

    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), nullable=False)
    comment = db.Column(db.String(300), nullable=False)
    movie_name = db.Column(db.String(120), nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())


db.create_all()


@app.route("/", methods=["POST", "GET"])
def hello_world():
    """Returns root endpoint HTML"""

    return render_template(
        "login.html",
    )


@app.route("/home_page", methods=["POST", "GET"])
@login_required
def home_page():
    """Returns root endpoint HTML"""

    if request.method == "POST":
        chosen_movie = request.form.get("chosen_movie")
    else:
        chosen_movie = ""

    movie_data = get_movie_data(chosen_movie)

    chosen_movie = movie_data["movie_id"]

    ratings = Rating.query.filter_by(movie_name=chosen_movie).all()

    if len(ratings) == 0:
        avg_rating = 0
    else:
        num_ratings = len(ratings)

        ratings_total = 0

        for i in range(num_ratings):
            ratings_total += ratings[i].rating

        avg_rating = "{:.1f}".format(ratings_total / num_ratings)

    comments = Comment.query.filter_by(movie_name=chosen_movie).all()
    num_comments = len(comments)

    print(chosen_movie)
    return render_template(
        "index.html",
        avg_rating=avg_rating,
        comments=comments,
        num_comments=num_comments,
        movie_id=movie_data["movie_id"],
        name=movie_data["name"],
        overview=movie_data["overview"],
        genres=movie_data["genre"],
        img_url=movie_data["image_url"],
        wiki_link=movie_data["wiki_link"],
        similar_movie_ids=movie_data["similar_movie_ids"],
        similar_movies=movie_data["similar_movies"],
        similar_posters=movie_data["similar_posters"],
        user_name=current_user.user_name,
    )


@app.route("/home_page_reload", methods=["POST", "GET"])
@login_required
def home_page_reload():
    """Returns root endpoint HTML"""

    chosen_movie = request.form.get("movie_id")
    rating = request.form.get("rate")

    comment = request.form.get("comment")
    if rating is not None:
        if Rating.query.filter_by(
            user_name=current_user.user_name, movie_name=chosen_movie
        ).first():
            flash("You've already rated this movie. Rate another one!")
        else:
            new_rating = Rating(
                user_name=current_user.user_name, rating=rating, movie_name=chosen_movie
            )
            db.session.add(new_rating)
            db.session.commit()
    elif comment is not None:

        new_comment = Comment(
            user_name=current_user.user_name,
            movie_name=chosen_movie,
            comment=comment,
        )
        db.session.add(new_comment)
        db.session.commit()

    ratings = Rating.query.filter_by(movie_name=chosen_movie).all()

    if len(ratings) == 0:
        avg_rating = 0
    else:
        num_ratings = len(ratings)

        ratings_total = 0

        for i in range(num_ratings):
            ratings_total += ratings[i].rating

        avg_rating = "{:.1f}".format(ratings_total / num_ratings)

    comments = Comment.query.filter_by(movie_name=chosen_movie).all()
    num_comments = len(comments)

    movie_data = get_movie_data(chosen_movie)

    return render_template(
        "index.html",
        avg_rating=avg_rating,
        comments=comments,
        num_comments=num_comments,
        movie_id=chosen_movie,
        name=movie_data["name"],
        overview=movie_data["overview"],
        genres=movie_data["genre"],
        img_url=movie_data["image_url"],
        wiki_link=movie_data["wiki_link"],
        similar_movie_ids=movie_data["similar_movie_ids"],
        similar_movies=movie_data["similar_movies"],
        similar_posters=movie_data["similar_posters"],
        user_name=current_user.user_name,
    )


@app.route("/signup", methods=["POST", "GET"])
def signup():
    """Adds user to database if not already in it and returns main page"""
    if request.method == "POST":
        user_name = request.form.get("user_name")
        password = request.form.get("password")

    user = User.query.filter_by(user_name=user_name).first()

    if user:
        flash("Email address already exists. Try logging in")
        return redirect(url_for("login"))

    new_user = User(
        user_name=user_name, password=generate_password_hash(password, method="sha256")
    )

    db.session.add(new_user)
    db.session.commit()

    return redirect("/login")


@app.route("/login")
def login():
    """Return main page after successful login"""
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():

    if request.form.get("signup") == "signup":
        return render_template("signup.html")

    user_name = request.form.get("user_name")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(user_name=user_name).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("login"))

    login_user(user, remember=remember)

    return redirect("/home_page")


@app.route("/wiki")
@login_required
def wiki_page():
    """Returns wiki endpoint HTML"""
    return render_template("wiki.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
    )
