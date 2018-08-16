# 1. Search for song on Genius by "[title] by [artist]"
# 2. Extract song ID from results
# 3. Follow song path to Genius wepage, extract lyrics from 'lyrics' div w/ BS4


import requests

import sys


def getGeniusAPIClientAccessToken():
    return "k5CSZxHK2TzAVzU17gC346jF1KKqAR3hha-O8qEgODSKnskgWUwdYjRIwOMWVIAS"


def getGeniusBaseURL():
    return "http://api.genius.com"


def createSongByArtistSearchTerm(song_title, song_artist):
    search_term = song_title + " by " + song_artist
    return search_term


# meta: "meta" object from Genius API response
def checkResponseStatus(meta):
    status = meta["status"]
    return status


def searchGeniusBySongTitleAndArtist(song_title, song_artist):
    # prepare GET request params
    access_token = getGeniusAPIClientAccessToken()
    headers = {"Authorization": "Bearer " + access_token}
    base_url = getGeniusBaseURL()
    search_url = base_url + "/search"
    search_term = createSongByArtistSearchTerm(song_title, song_artist)
    full_url = search_url + "?q=" + search_term

    # GET request
    response = requests.get(full_url, headers=headers)
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


def test():
    print("Starting test")
    song = sys.argv[1]
    artist = sys.argv[2]
    #  song = "oops"
    #  artist = "Britney Spears"
    print("Searching for", song, " by ", artist)
    response_json = searchGeniusBySongTitleAndArtist(song, artist)
    print("Response JSON:")
    print(response_json)
    for hit in response_json["response"]["hits"]:
        if checkArtistsMatch(artist, hit["result"]):
            print("Found matching result")
            print("Matching song name: ", hit["result"]["title"])
            print("Path to matching song lyrics: ", hit["result"]["path"])


if __name__ == "__main__":
    test()
