import os
import random
import requests
from dotenv import load_dotenv, find_dotenv

from wiki import get_wiki_link

load_dotenv(find_dotenv()) # This is to load your API keys from .env

BASE_URL = 'https://api.themoviedb.org/3/movie/'

def get_similar_movies(chosen_movie, params):
    """ Gets similar movies to passed in movie id from TMDB server """
    response = requests.get(BASE_URL + chosen_movie + "/similar", params=params)
    data = response.json()
    similar_movie_ids = []
    similar_movies = []
    similar_posters = []

    for i in range(4):
        similar_movie_ids.append(data['results'][i]['id'])
        similar_movies.append(data['results'][i]['original_title'])
        similar_posters.append(
            'https://image.tmdb.org/t/p/w185' +
            data['results'][i]['poster_path']
            )

    return similar_movie_ids, similar_movies, similar_posters


def get_movie_data(chosen_movie):
    """ Chooses randomly from list of movie ids to do a get from TMDB's server """

    movie_ids = [
        '157336',
        '12445',
        '9476',
        '157350',
        '262504',
        '262500',
        '70160',
        '101299',
        '198663'
    ]
    params = {
        'api_key': os.getenv('TMDB_KEY'),
    }
    if chosen_movie == '':
        chosen_movie = random.choice(movie_ids)

    response = requests.get(BASE_URL + chosen_movie, params=params)
    data = response.json()


    wiki_link = get_wiki_link(data['original_title'])
    similar_movie_ids, similar_movies, similar_posters = get_similar_movies(chosen_movie, params)

    genre_list = data['genres']
    genre_names = [d['name'] for d in genre_list]
    return {
        'name': data['original_title'],
        'overview': data['tagline'],
        'genre': genre_names,
        'image_url': 'https://image.tmdb.org/t/p/w500' + data['poster_path'],
        'wiki_link': wiki_link,
        'similar_movie_ids': similar_movie_ids,
        'similar_movies': similar_movies,
        'similar_posters': similar_posters,
    }
