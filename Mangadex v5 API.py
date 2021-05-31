import requests
import json

def listmanga(manga):
    parameters = {"title":manga}
    response = requests.get("https://api.mangadex.org/manga", params=parameters)
    print(response.status_code)
    dict = {}
    for i in range(response.json()["total"]):
        name = response.json()["results"][i]["data"]["attributes"]["title"]["en"]
        id = response.json()["results"][i]["data"]["id"]
        dict[f"{i}"] = [name, id]
    return dict

def getmanga(mangaid):
    response = requests.get(f"https://api.mangadex.org/manga/{mangaid}")
    print(response.status_code)
    dict = {}
    dict["name"] = response.json()["data"]["attributes"]["title"]["en"]
    dict["id"] = response.json()["data"]["id"]
    dict["rating"] = response.json()["data"]["attributes"]["contentRating"]
    dict["originallang"] = response.json()["data"]["attributes"]["originalLanguage"]
    dict["demographic"] = response.json()["data"]["attributes"]["publicationDemographic"]
    dict["status"] = response.json()["data"]["attributes"]["status"]
    return dict

def get_ch(mangaid, chapter):
    parameters = {"manga":mangaid,"chapter":chapter}
    response = requests.get(f"https://api.mangadex.org/chapter", params=parameters)
    print(response.status_code)
    dict = {}
    dict["chid"] = response.json()["results"][0]["data"]["id"]
    dict["filenames"] = response.json()["results"][0]["data"]["attributes"]["data"]
    dict["hash"] = response.json()["results"][0]["data"]["attributes"]["hash"]
    return dict

def getmdhomeurl(chid):
    response = requests.get(f"https://api.mangadex.org/at-home/server/{chid}")
    print(response.status_code)
    dict = {}
    dict["baseurl"] = response.json()["baseUrl"]
    return dict

def ch_constructor(manga, chapter):
    mangalist = listmanga(manga)
    print(mangalist["1"][0])
    mangaid = mangalist["1"][1]
    print(mangaid)
    ch_dict = get_ch(mangaid, chapter)
    chid = ch_dict["chid"]
    hash = ch_dict["hash"]
    filenames = ch_dict["filenames"]
    mdhomeurl = getmdhomeurl(chid)
    baseurl = mdhomeurl["baseurl"]
    dict = {}
    i = 1
    for file in filenames:
        dict[f"page {i}"] = f"{baseurl}/data/{hash}/{file}"
        i = i + 1
    return dict
