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

    pc(_json)

    results = []

    #extract data from server response
    for item in _json["data"]:
        results.append({
            "title": item["attributes"]["title"]["en"],
            "mangaid": item["id"],
            "desc": item["attributes"]["description"]["en"],
            "originalLanguage": item["attributes"]["originalLanguage"],
            "lastVolume": item["attributes"]["lastVolume"],
            "lastChapter": item["attributes"]["lastChapter"],
            "publicationDemographic": item["attributes"]["publicationDemographic"],
            "status": item["attributes"]["status"],
            "contentRating": item["attributes"]["contentRating"]
            })

    return results


#get details of a manga using its id
def view_manga(mangaid):
    """View details about manga using its id.
    
    Get all data about a maga using its id."""

    #make query to server to get a dict of manga
    response = requests.get(apiurl + "manga/" + mangaid)
    _json = response.json()

    pc(_json)

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
    """Get a list of all tags used by Mangadex and their id."""

    #make query to server to get list of all tags with their id
    response = requests.get(apiurl + "manga/tag")
    _json = response.json()

    return pformat(_json)


#get list of cover arts
def cover_art_list(mangaid):
    """Get a list of all cover arts for a manga using its
    id(manga's id) and some extra details about the cover art."""

    #make query to server to get dict of cover arts
    parameters = {
        "manga[]": mangaid
    }
    response = requests.get(apiurl + "cover", params = parameters)
    _json = response.json()

    #extract data from server response
    results = []

    pc(_json)

    for item in _json["data"]:
        results.append({
                "fileName": item["attributes"]["fileName"],
                "version": item["attributes"]["version"],
                "volume": item["attributes"]["volume"],
                "coverid": item["id"]
            })

    return results


#construct cover urls
def get_cover_urls(mangaid, size = None):
    """Get cover art urls for all cover arts of a manga.
    This function uses the `cover_art_list` function and returns
    the full constructed urls but not any data about the cover art.
    
    Leave size argument empty for full quality or `512`
    for 512px quality or `256` for 256px quality.
    512 and 256 are best for thumbnails."""

    #get cover art list for manga
    coverdata = cover_art_list(mangaid)

    pc(coverdata)

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
