# Program to read lyrics from Genius page for given song
# All credit for retrieving song title goes to www.github.com/XanderMJ
# I referenced https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/
#   for help getting the lyrics from the api

import sys
import re
import requests
from bs4 import BeautifulSoup

client_access_token = '08HrtqWY7Cis5zUlL49S5R3QHHA5q5gUCaEzZzVYY6XgNvnJRHTN0Jx86H9xqWam'

def get_lyrics(song):
    song = song.split(" - ")
    song_title = song[0]
    artist_name = song[1]

    base_url = "https://api.genius.com"
    search_url = base_url + "/search"
    headers = {'Authorization': 'Bearer ' + client_access_token}
    data = {'q': song_title}
    response = requests.get(search_url, data=data, headers=headers)
    json = response.json()
    song_info = None
    for hit in json["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"] == artist_name:
            song_info = hit
            break
    if song_info:
        song_api_path = song_info["result"]["api_path"]
        song_url = base_url + song_api_path
        response = requests.get(song_url, headers=headers)
        json = response.json()
        path = json["response"]["song"]["path"]
        page_url = "https://genius.com" + path
        page = requests.get(page_url)
        html = BeautifulSoup(page.text, "html.parser")
        [h.extract() for h in html('script')]
        lyrics = html.find("div", class_="lyrics").get_text()
        return lyrics

# Some people online say this is wrong, but it definitely fixes some problems
reload(sys)
sys.setdefaultencoding('utf8')

# get_lyrics(spotilib.song_info())
# get_duration(spotilib.song_info())


# for testing purposes
if __name__ == "__main__":
   print get_lyrics("Firebird - Galantis")