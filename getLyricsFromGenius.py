# 1. Search for song on Genius by "[title] by [artist]"
# 2. Extract song ID from results
# 3. Follow song path to Genius wepage, extract lyrics from 'lyrics' div w/ BS4


import pickle
import requests
from bs4 import BeautifulSoup

import re


def loadCredentials(credentials_pickle_file):
    try:
        with open(credentials_pickle_file, 'rb') as c:
            return pickle.load(c)
    except IOError:
        print("Error: Couldn't open credentials file. Exiting")


def getGeniusAPIBaseURL():
    return "http://api.genius.com"


# meta: "meta" object from Genius API response
def getResponseStatus(response):
    status = response["meta"]["status"]
    return status


def createSearchGETRequestURLs(song_title, song_artist):
    """
    Creates a list of search URLs, each URL having a different variant of
    (title + artist).

    The variants are:
        1. "song_title by song_artist"
        2. "song_artist - song_title"
        3. Same as 2. but song_title has anything including and after  " - "
            removed.
        4. Same as 2, but song_title has anything in parentheses removed.

    If modifying song_title in a particular way would not change it, that
    variant is not appended to the list (e.g., if song_title does not contain
    a '-', variant #3 is not created nor appended to the end of the list.

    Returns:
        full_urls: a list of search URLs corresponding to the search terms
    """
    search_terms = []
    search_terms.append(song_title + " by " + song_artist)

    search_term_base = song_artist + " - "
    search_terms.append(search_term_base + song_title)  # Variant #2

    # Variant #3
    if "-" in song_title:
        hyphen = "\ -\ .*"
        hyphen_title = re.sub(hyphen, "", song_title)
        search_terms.append(search_term_base + hyphen_title)

    # Variant #4
    if "(" in song_title:
        parens = "\ \(.*\)"
        parens_title = re.sub(parens, "", song_title)
        search_terms.append(search_term_base + parens_title)

    base_url = getGeniusAPIBaseURL()
    search = "/search?q="
    full_urls = [base_url + search + term for term in search_terms]
    print("All search URLs: ", "\n".join(full_urls))
    return full_urls


def prepareGETRequestHeaders():
    credentials = loadCredentials("credentials.p")
    access_token = credentials["GENIUS_API_CLIENT_TOKEN"]
    headers = {"Authorization": "Bearer " + access_token}
    return headers


def searchGenius(search_url):
    """
    Searches the Genius API with a variety of search terms until it finds a hit
    with a matching artist.

    Parameters:
        search_url: URL to GET

    Returns:
        response_json: JSON object containing info about target song
    """
    # GET request params
    headers = prepareGETRequestHeaders()

    # actual GET request
    response = requests.get(search_url, headers=headers)
    response_json = response.json()
    return response_json


def checkTitlesMatch(song_title, search_result):
    result_title = search_result["title"]

    # Let's not let capitalization fool us
    result_lower = result_title.lower()
    song_lower = song_title.lower()

    # Remove any ' - ' and anything aftwards
    song_minus_hyphen = re.sub("\ -\ .*", "", song_lower)

    # Remove any '()' and anything inbetween
    song_minus_parens = re.sub("\ \(.*\)", "", song_minus_hyphen)
    result_minus_parens = re.sub("\ \(.*\)", "", result_lower)

    if song_minus_parens == result_minus_parens:
        return True
    return False


def checkArtistsMatch(song_artist, search_result):
    result_artist = search_result["primary_artist"]["name"]

    # "Zedd & Liam Payne" was the listed primary artist or "Get Low",
    # so I changed this from "==" to "in" (to make "Zedd" as the Spotify artst
    # satisfy the condition). This might actually be worse in the long run, but
    # for now it seems to be a good fix.

    # Let's not let capitalization fool us
    result_lower = result_artist.lower()
    song_lower = song_artist.lower()

    # Remove any '&' and anything afterwards
    song_minus_amp = re.sub("\&.*", "", song_lower)
    if song_minus_amp in result_lower:
        return True
    return False


# search_result: "result" JSON from Genius API /search GET request
# (search_result is one "result" in the "hits" list)
def extractSongPathFromGeniusSearchResult(search_result):
    return search_result["path"]


def findMatchingHitInSearchResults(song_title, song_artist, search_results):
    """
    Looks for a hit in search_results with a primary artist that matches
    artist.

    Parameters:
        song_title: title to match
        song_artist: artist to match
        search_results: JSON object with list of hits

    Returns:
        "result" field of matching hit in JSON object
    """
    for hit in search_results["response"]["hits"]:
        artist_match = checkArtistsMatch(song_artist, hit["result"])
        title_match = checkTitlesMatch(song_title, hit["result"])
        if artist_match and title_match:
            return hit["result"]
    return None


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
