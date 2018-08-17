# 1. Search for song on Genius by "[title] by [artist]"
# 2. Extract song ID from results
# 3. Follow song path to Genius wepage, extract lyrics from 'lyrics' div w/ BS4


import pickle
import requests
from bs4 import BeautifulSoup

import sys


def loadCredentials():
    try:
        with open('credentials.p', 'rb') as c:
            return pickle.load(c)
    except IOError:
        print("Error: Couldn't open credentials file. Exiting")


def getGeniusAPIBaseURL():
    return "http://api.genius.com"


# meta: "meta" object from Genius API response
def getResponseStatus(response):
    status = response["meta"]["status"]
    return status


def createSongByArtistSearchTerm(song_title, song_artist):
    search_term = song_title + " by " + song_artist
    return search_term


def createFullSearchGETRequestURL(song_title, song_artist):
    base_url = getGeniusAPIBaseURL()
    search = "/search?q="
    search_term = createSongByArtistSearchTerm(song_title, song_artist)
    full_url = base_url + search + search_term
    return full_url


def prepareGETRequestHeaders():
    credentials = loadCredentials()
    access_token = credentials["GENIUS_API_CLIENT_TOKEN"]
    headers = {"Authorization": "Bearer " + access_token}
    return headers


def searchGeniusBySongTitleAndArtist(song_title, song_artist):
    # GET request params
    search_url = createFullSearchGETRequestURL(song_title, song_artist)
    headers = prepareGETRequestHeaders()

    # actual GET request
    response = requests.get(search_url, headers=headers)
    response_json = response.json()
    return response_json


# artist_name: actual artist name from Spotify
# search_result: "result" JSON representing one song
# (search_result is one "result" in the "hits" list)
def checkArtistsMatch(artist_name, search_result):
    result_artist = search_result["primary_artist"]["name"]
    if artist_name == result_artist:
        return True
    return False


# search_result: "result" JSON from Genius API /search GET request
# (search_result is one "result" in the "hits" list)
def extractSongPathFromGeniusSearchResult(search_result):
    return search_result["path"]


def getGeniusWebsiteBaseURL():
    return "https://genius.com"


def getLyricsPageHTMLFromPath(song_path):
    lyrics_url = getGeniusWebsiteBaseURL() + song_path
    page_html = requests.get(lyrics_url)
    return page_html


def parseLyricsPageHTML(html):
    html_text = BeautifulSoup(html.text, "html.parser")
    #  [h.extract() for h in lyrics_html('script')]
    lyrics = html_text.find("div", class_="lyrics").get_text()
    return lyrics


def test():
    print("Starting test")
    song = sys.argv[1]
    artist = sys.argv[2]
    #  song = "oops"
    #  artist = "Britney Spears"
    print("Searching for", song, "by", artist)
    response_json = searchGeniusBySongTitleAndArtist(song, artist)
    status = getResponseStatus(response_json)
    if status != 200:
        print("Error: GET returned", status)
        print("Exiting.")
        sys.exit()
    print("Response JSON:")
    print(response_json)
    song_path = ""
    for hit in response_json["response"]["hits"]:
        if checkArtistsMatch(artist, hit["result"]):
            print("Found matching result")
            print("Matching song name: ", hit["result"]["title"])
            song_path = extractSongPathFromGeniusSearchResult(hit["result"])
            print("Path to matching song lyrics: ", song_path)
            break
    lyrics_page_html = getLyricsPageHTMLFromPath(song_path)
    lyrics = parseLyricsPageHTML(lyrics_page_html)
    print("lyrics: ", lyrics)


if __name__ == "__main__":
    test()
