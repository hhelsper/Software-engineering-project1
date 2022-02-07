

def get_wiki_link(title):
    import requests
    S = requests.Session()

    URL = "https://en.wikipedia.org/w/api.php"

    SEARCHPAGE = title + ' movie'

    PARAMS = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": SEARCHPAGE
    }

    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    pageId = DATA['query']['search'][0]['pageid']
    return 'https://en.wikipedia.org/?curid=' + str(pageId)