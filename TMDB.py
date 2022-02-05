import collections
import requests
import os
#import more_itertools as mt
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
        #'movie_id': random.choice(movie_ids),
        'api_key': os.getenv('TMDB_KEY'),
    }


    response = requests.get(BASE_URL + random.choice(movie_ids), params=params)
    data = response.json()
    
    #articles = data['response']['docs']
    def flatten(x):
        if isinstance(x, dict) :
            return [x]
        elif isinstance(x, collections.Iterable) :
            return [a for i in x for a in flatten(i)]
        else:
            return [x]

    genre_list = [data['genres']]
    list = flatten(genre_list)
    print(len(list))
    #[d['name'] for d in mt.collapse(genre_list, base_type=dict)]
    genre_names = [d['name'] for d in list]
    
    #for genre in len(data['genres']):
        #genre_list.append(genre)
   
    
    return {
        #data
        'name': data['original_title'],
        'overview': data['tagline'],
        'genre': genre_names
    }
num = get_movie_data()
print(num)