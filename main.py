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
from flask import Flask, render_template, request, redirect, url_for, flash
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

# three lines of code necessary for flask login
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
    # automatically generated timestamp for each comment which will display next to comment
    time_created = db.Column(db.DateTime(timezone=True), server_default=func.now())


# creates all db models
db.create_all()

# base route of web app that starts user at the login page
@app.route("/", methods=["POST", "GET"])
def hello_world():
    """Returns root endpoint HTML"""

    return render_template(
        "login.html",
    )


# this is the route for the first main page loaded
@app.route("/home_page", methods=["POST", "GET"])
@login_required
def home_page():
    """Returns root endpoint HTML"""
    # if else statment to see if movie was selected from similar movies and set var to that movie id
    if request.method == "POST":
        chosen_movie = request.form.get("chosen_movie")
    else:
        chosen_movie = ""

    # makes a call to tmdb db to get all required data on currently displayed movie
    movie_data = get_movie_data(chosen_movie)

    # stores tmdb movie id to pass back to html
    chosen_movie = movie_data["movie_id"]

    # queries all ratings in db
    ratings = Rating.query.filter_by(movie_name=chosen_movie).all()
    # sets average rating to 0 which is used in html to display text no ratings yet
    if len(ratings) == 0:
        avg_rating = 0
    else:
        num_ratings = len(ratings)

        ratings_total = 0
        # for loop to calculate the average ratings for movie and round to 1 dec point
        for i in range(num_ratings):
            ratings_total += ratings[i].rating

        avg_rating = "{:.1f}".format(ratings_total / num_ratings)

    comments = Comment.query.filter_by(movie_name=chosen_movie).all()
    num_comments = len(comments)

    # this return statement passes all the info along to the main html
    # so that the movie page plus ratings and comments can be rendered
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


# this is the route for the main page reload which I use
# to make sure the page does not auto refresh to another movie
# but stays on the movie just rated or commented on so that
# user can view the rating or comment just posted
@app.route("/home_page_reload", methods=["POST", "GET"])
@login_required
def home_page_reload():
    """This route and function takes in comment or rating and posts it back to html"""

    chosen_movie = request.form.get("movie_id")
    rating = request.form.get("rate")

    comment = request.form.get("comment")
    # if else if statement to determine whether rating or comment has been posted back
    # if rating is returned this code saves rating to db
    if rating is not None:
        # if else statment to disallow user to rate movies more than once
        if Rating.query.filter_by(
            user_name=current_user.user_name, movie_name=chosen_movie
        ).first():
            flash("You've already rated this movie. Rate another one!")
        else:
            # saves first user rating to db
            new_rating = Rating(
                user_name=current_user.user_name, rating=rating, movie_name=chosen_movie
            )
            db.session.add(new_rating)
            db.session.commit()
    # if comment returned this code saves the comment to the db
    elif comment is not None:

        new_comment = Comment(
            user_name=current_user.user_name,
            movie_name=chosen_movie,
            comment=comment,
        )
        db.session.add(new_comment)
        db.session.commit()

    ratings = Rating.query.filter_by(movie_name=chosen_movie).all()
    # sets average rating to 0 which is used in html to display text no ratings yet
    if len(ratings) == 0:
        avg_rating = 0
    else:
        num_ratings = len(ratings)

        ratings_total = 0
        # for loop to calculate the average ratings for movie and round to 1 dec point
        for i in range(num_ratings):
            ratings_total += ratings[i].rating

        avg_rating = "{:.1f}".format(ratings_total / num_ratings)

    # these two lines get and store all comments and the set the length of total comments
    comments = Comment.query.filter_by(movie_name=chosen_movie).all()
    num_comments = len(comments)

    # makes a call to tmdb db to get all required data on currently displayed movie
    movie_data = get_movie_data(chosen_movie)

    # this return statement passes all the info along to the main html
    # so that the movie page plus ratings and comments can be rendered
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

    # checks to see if user name for signup is already in database
    user = User.query.filter_by(user_name=user_name).first()

    # if user exists flash message and redirect to login
    if user:
        flash("Email address already exists. Try logging in")
        return redirect(url_for("login"))

    # if user doesn't exist in db these three lines of code adds user to db
    new_user = User(
        user_name=user_name, password=generate_password_hash(password, method="sha256")
    )

    db.session.add(new_user)
    db.session.commit()

    # takes user back to login screen so they can now login after being saved to db
    return redirect("/login")


@app.route("/login")
def login():
    """Return main page after successful login"""
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    """Method with logic for logging user in"""
    # if signup button clicked in html user directed to signup page
    if request.form.get("signup") == "signup":
        return render_template("signup.html")

    # pulls username and password from html form
    user_name = request.form.get("user_name")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    # query variable used to check if user is in database
    user = User.query.filter_by(user_name=user_name).first()
    # if statement checks if username is in db and password for that user matches
    if not user or not check_password_hash(user.password, password):
        flash("Please check your login details and try again.")
        return redirect(url_for("login"))

    # flask_login login user method with user info passed in
    login_user(user, remember=remember)

    # takes signed in user to homepage
    return redirect("/home_page")


@app.route("/wiki")
@login_required
def wiki_page():
    """Returns wiki endpoint HTML"""
    return render_template("wiki.html")


@app.route("/logout")
@login_required
def logout():
    """Function to log user  out and redirect to login page"""
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "0.0.0.0"), port=int(os.getenv("PORT", "8080")), debug=True
    )
