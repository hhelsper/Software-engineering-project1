import collections
import requests
import os
import random
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv()) # This is to load your API keys from .env

BASE_URL = 'https://api.themoviedb.org/3/movie/'



def get_movie_data():
    """ Returns a list of headlines about a given topic """

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

    chosen_movie = random.choice(movie_ids)
    response = requests.get(BASE_URL + chosen_movie, params=params)
    data = response.json()
    
    
    
 

    genre_list = data['genres']
    

    genre_names = [d['name'] for d in genre_list]
    
    return {
        
        'name': data['original_title'],
        'overview': data['tagline'],
        'genre': genre_names,
        'image_url': 'https://image.tmdb.org/t/p/w500' + data['poster_path']
    }


