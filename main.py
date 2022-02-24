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
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

login_manager = LoginManager()
login_manager.login_view = "hello_world"
login_manager.init_app(app)

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return "<User %r" % self.user_name

    def get_username(self):
        return self.user_name

    def get_id(self):
        return self.user_id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Rating(db.Model):
    __tablename__ = "rating"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Integer, db.ForeignKey("user.user_name"))
    rating = db.Column(db.Integer, nullable=False)
    movie_name = db.Column(db.String(120), nullable=False)


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.Integer, db.ForeignKey("user.user_name"))
    comment = db.Column(db.String(300), nullable=False)
    movie_name = db.Column(db.String(120), nullable=False)
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    wiki_link = db.Column(db.String(300), nullable=False)


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

    print(chosen_movie)
    return render_template(
        "index.html",
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

    print("chosen movie:" + request.form.get("movie_id"))
    movie_data = get_movie_data(chosen_movie)

    return render_template(
        "index.html",
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
    # login code goes here
    if request.form.get("signup") == "signup":
        return render_template("signup.html")

    user_name = request.form.get("user_name")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(user_name=user_name).first()

    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("login"))

    movie_data = get_movie_data("")

    login_user(user, remember=remember)

    return redirect("/home_page")


@app.route("/wiki")
@login_required
def wiki_page():
    """Returns wiki endpoint HTML"""
    return render_template("wiki.html")


# @app.route("/comments", methods=["GET", "POST"])
# @login_required
# def comments():
#     """Returns wiki endpoint HTML"""

#     if request.method == "POST":
#         data = request.form
#         comment = Comment(
#             comment=data["comment"],
#             wiki_link=data["wiki_link"],
#             movie_name=data["movie_name"],
#             user_name=current_user.user_name,
#         )
#     return render_template(
#         "comments.html",
#     )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
    )
