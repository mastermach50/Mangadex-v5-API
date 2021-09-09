import requests
import pyperclip
from PIL import Image
from io import BytesIO
from pprint import pprint, pformat

apiurl = "https://api.mangadex.org/"
uploadsapiurl = "https://uploads.mangadex.org/"

#temp===========================
def pc(obj):
    pprint(obj)
    pyperclip.copy(pformat(obj))
#temp===========================

#search for manga using their title
def search(name, rating = "default", limit = 10):
    """Search for manga using their title to receive list of search results along with
    details about them such as mangaid, description, status etc.

    Content rating and output limit can be defined.
    Shorthand ratings are `default`/ `all`/ `clean`, full rating is a list which can have
    `safe`, `suggestive`, `erotica`, `pornographic`
    
    eg: rating = ["safe","suggestive","erotica"]"""

    #content rating
    if rating == "default":
        ratings = ["safe","suggestive","erotica"]
    elif rating == "all":
        ratings = ["safe","suggestive","erotica","pornographic"]
    elif rating == "clean":
        ratings = ["safe","suggestive"]
    elif isinstance(rating, list):
        ratings = rating
    else:
        ratings = ["safe","suggestive","erotica"]

    #limit
    if limit > 100:
        limit = 100

    #make query to server to get a list of results
    parameters = {
        "title": name,
        "contentRating[]": ratings,
        "limit": limit
    }
    response = requests.get(url = apiurl + "manga", params = parameters)
    _json = response.json()

    results = []

    #extract data from server response
    for item in _json["results"]:
        results.append({
            "title": item["data"]["attributes"]["title"]["en"],
            "mangaid": item["data"]["id"],
            "desc": item["data"]["attributes"]["description"]["en"],
            "originalLanguage": item["data"]["attributes"]["originalLanguage"],
            "lastVolume": item["data"]["attributes"]["lastVolume"],
            "lastChapter": item["data"]["attributes"]["lastChapter"],
            "publicationDemographic": item["data"]["attributes"]["publicationDemographic"],
            "status": item["data"]["attributes"]["status"],
            "contentRating": item["data"]["attributes"]["contentRating"]
            })

    return results


#get details of a manga using its id
def view_manga(mangaid):
    """View details about manga using their id"""

    #make query to server to get a dict of manga
    response = requests.get(apiurl + "manga/" + mangaid)
    _json = response.json()

    #extract data from server response
    result = {
        "title": _json["data"]["attributes"]["title"]["en"],
        "mangaid": _json["data"]["id"],
        "desc": _json["data"]["attributes"]["description"]["en"],
        "originalLanguage": _json["data"]["attributes"]["originalLanguage"],
        "lastVolume": _json["data"]["attributes"]["lastVolume"],
        "lastChapter": _json["data"]["attributes"]["lastChapter"],
        "publicationDemographic": _json["data"]["attributes"]["publicationDemographic"],
        "status": _json["data"]["attributes"]["status"],
        "contentRating": _json["data"]["attributes"]["contentRating"]
        }

    return result


#get list of all tags
def tags():

    #make query to server to get list of all tags with their id
    response = requests.get(apiurl + "manga/tag")
    _json = response.json()

    return pformat(_json)


#get list of cover arts
def cover_art_list(mangaid):

    #make query to server to get dict of cover arts
    parameters = {
        "manga[]": mangaid
    }
    response = requests.get(apiurl + "cover", params = parameters)
    _json = response.json()

    #extract data from server response
    results = []

    for item in _json["results"]:
        results.append({
                "fileName": item["data"]["attributes"]["fileName"],
                "version": item["data"]["attributes"]["version"],
                "volume": item["data"]["attributes"]["volume"],
                "coverid": item["data"]["id"]
            })

    return results


#construct cover urls
def get_cover_urls(mangaid, size = "original"):
    """"""
    #get cover art list for manga
    coverdata = cover_art_list(mangaid)

    #construct urls
    results = []

    #decide file size
    if size == "512":
        end = ".512.jpg"
    elif size == "256":
        end = ".256.jpg"
    else:
        end = ""

    for item in coverdata:
        results.append(uploadsapiurl + "/covers/"+ mangaid + "/" + item["fileName"])

    return results


if __name__ == "__main__":
    {'title': "You, The Assassin, Can't Kill", 'mangaid': '9277cf92-588b-4198-b6a9-16f8a06320d9'}
    for item in get_cover_urls("9277cf92-588b-4198-b6a9-16f8a06320d9"):
        response = requests.get(item)
        img = Image.open(BytesIO(response.content))
        img.show()
