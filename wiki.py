"""This file contains method to make wiki api call"""
import requests

# method takes in title of movie to query wiki link for
def get_wiki_link(title):
    """This makes a call to the wikipedia API"""
    session = requests.Session()

    url = "https://en.wikipedia.org/w/api.php"

    search = title + " movie"

    params = {"action": "query", "format": "json", "list": "search", "srsearch": search}

    response = session.get(url=url, params=params)
    data = response.json()
    page_id = data["query"]["search"][0]["pageid"]
    # returns wikipedia link for chosen movie
    return "https://en.wikipedia.org/?curid=" + str(page_id)
