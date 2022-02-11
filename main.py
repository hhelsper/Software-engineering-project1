import os
from tmdb_api_call import get_movie_data
from flask import Flask, render_template, request


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



@app.route('/', methods=["POST", "GET"])
def hello_world():
    """ Returns root endpoint HTML """
    if request.method == "POST":
        chosen_movie = request.form.get("chosen_movie")
    else:
        chosen_movie = ''


    movie_data = get_movie_data(chosen_movie)

    return render_template(
        "index.html",
        name =movie_data['name'],
        overview =movie_data['overview'],
        genres = movie_data['genre'],
        img_url = movie_data['image_url'],
        wiki_link = movie_data['wiki_link'],
        similar_movie_ids = movie_data['similar_movie_ids'],
        similar_movies = movie_data['similar_movies'],
        similar_posters = movie_data['similar_posters'],
        )


@app.route('/wiki')
def wiki_page():
    """ Returns wiki endpoint HTML """
    return render_template(
        "wiki.html",
    )


app.run(
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', '8080')),
    debug=True
)
