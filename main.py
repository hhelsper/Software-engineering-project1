import os

from flask import Flask, render_template
from TMDB import get_movie_data

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def hello_world():
    """ Returns root endpoint HTML """




    
    movie_data = get_movie_data()
    
    return render_template(
        "index.html",
        
        name =movie_data['name'],
        overview =movie_data['overview'],
        genres = movie_data['genre'],
        img_url = movie_data['image_url']
    )

app.run(
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080)),
    debug=True
)