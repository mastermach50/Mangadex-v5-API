from typing import Optional
import requests
import json

class Mangadex:
    def __init__(self, manga):
        self.manga = manga
        self.mangaid = None
        self.chapter = 1
        self.chapterid = None
        self.chapterhash = None
        self.chapterbaseurl = None
        self.searchresults = {}

    def listmanga(self):
        parameters = {"title":self.manga}
        response = requests.get("https://api.mangadex.org/manga", params=parameters)
        self.searchresults = {}
        for i in range(response.json()["total"]):
            name = response.json()["results"][i]["data"]["attributes"]["title"]["en"]
            id = response.json()["results"][i]["data"]["id"]
            self.searchresults[f"{i}"] = [name, id]
        self.manga = self.searchresults["0"][0]
        self.mangaid = self.searchresults["0"][1]

    def getmanga(self):
        response = requests.get(f"https://api.mangadex.org/manga/{self.mangaid}")
        self.searchresults = {}
        self.searchresults["name"] = response.json()["data"]["attributes"]["title"]["en"]
        self.searchresults["id"] = response.json()["data"]["id"]
        self.searchresults["rating"] = response.json()["data"]["attributes"]["contentRating"]
        self.searchresults["originallang"] = response.json()["data"]["attributes"]["originalLanguage"]
        self.searchresults["demographic"] = response.json()["data"]["attributes"]["publicationDemographic"]
        self.searchresults["status"] = response.json()["data"]["attributes"]["status"]

    def get_ch(self, chapter):
        self.chapter = chapter
        parameters = {"manga":self.mangaid,"chapter":str(self.chapter)}
        response = requests.get(f"https://api.mangadex.org/chapter", params=parameters)
        self.searchresults = {}
        self.searchresults["chid"] = response.json()["results"][0]["data"]["id"]
        self.searchresults["filenames"] = response.json()["results"][0]["data"]["attributes"]["data"]
        self.searchresults["hash"] = response.json()["results"][0]["data"]["attributes"]["hash"]
        self.chapterid = self.searchresults["chid"]
        self.chapterhash = self.searchresults["hash"]
        self.filenames = self.searchresults["filenames"]

    def getmdhomeurl(self):
        response = requests.get(f"https://api.mangadex.org/at-home/server/{self.chapterid}")
        self.searchresults = {}
        self.searchresults["baseurl"] = response.json()["baseUrl"]
        self.chapterbaseurl = self.searchresults["baseurl"]

    def ch_constructor(self, chapter):
        if chapter != None:
            self.chapter = chapter
        else:
            pass
        self.listmanga()
        print(self.manga)
        print(self.mangaid)
        self.get_ch(self.chapter)
        print(self.chapter)
        print(self.chapterid)
        self.getmdhomeurl()
        self.searchresults = {}
        i = 1
        for file in self.filenames:
            self.searchresults[f"page {i}"] = f"{self.chapterbaseurl}/data/{self.chapterhash}/{file}"
            i = i + 1
