from bs4 import BeautifulSoup
import pickle
import re
import requests


def loadCredentials(credentials_pickle_file):
    """Get the Genius API credentials by loading a pickle file.

    Args:
        credentials_pickle_file (str): Path to pickle file containing creds.

    Returns:
        dict: dictionary containing API keys, token, etc.

    """
    try:
        with open(credentials_pickle_file, 'rb') as c:
            return pickle.load(c)
    except IOError:
        print("Error: Couldn't open credentials file. Exiting.")


def getGeniusAPIBaseURL():
    return "http://api.genius.com"


# meta: "meta" object from Genius API response
def getResponseStatus(response):
    status = response["meta"]["status"]
    return status


def createSearchGETRequestURLs(song_title, song_artist):
    """Create a list of search URLs, each with a variant of (title + artist).

    The variants are:
        1. "song_title by song_artist"
        2. "song_artist - song_title"
        3. Same as 2. but song_title has anything including and after  " - "
            removed.
        4. Same as 2, but song_title has anything in parentheses removed.

    If modifying song_title in a particular way would not change it, that
    variant is not appended to the list (e.g., if song_title does not contain
    a '-', variant #3 is not created nor appended to the end of the list.

    Args:
        song_title (str): Title of song whose lyrics we want.
        song_artist (str): Artist of song whose lyrics we want.

    Returns:
        list of str: search URLs corresponding to the search terms
    """
    # Variant #1
    search_terms = []
    search_terms.append(song_title + " by " + song_artist)

    # Variant #2
    search_term_base = song_artist + " - "
    search_terms.append(search_term_base + song_title)

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

    #  print("All search URLs: ", "\n".join(full_urls))
    return full_urls


def prepareGETRequestHeaders():
    """Create headers for GET request, which includes the API Client token."""
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
        JSON-format dict: JSON object containing info about target song

    """
    # GET request params
    headers = prepareGETRequestHeaders()

    # actual GET request
    response = requests.get(search_url, headers=headers)
    response_json = response.json()
    return response_json


def checkTitlesMatch(song_title, search_result):
    """Check to see if the current search result matches our song title.

    Before checking, we also remove any parentheses (and text inside) and any
    hyphens (and text following the hyphen).

    Args:
        song_title (str): The name of the song to be matched.
        search_result (JSON-format dict): JSON object containing song info.

    Returns:
        True if search_result corresponds to a song whose title matches.
        False otherwise.

    """
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
    """Check to see if the current search result matches our song artist.

    Before checking, we also remove any ampersands and anything afterwards.

    Args:
        song_artist (str): The artist of the song to be matched.
        search_result (JSON-format dict): JSON object containing song info.

    Returns:
        True if search_result corresponds to a song whose artist matches.
        False otherwise.

    """
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


def extractSongPathFromGeniusSearchResult(search_result):
    """Get the URL to the song lyrics out of the matching search result.

    Args:
        search_result (JSON-format dict): JSON object with info about a song.

    Returns:
        str: part of URL to page of song lyrics.

    """
    return search_result["path"]


def findMatchingHitInSearchResults(song_title, song_artist, search_results):
    """ Looks for a hit with a primary artist that matches artist.

    Args:
        song_title (str): Title of song that we are trying to match.
        song_artist (str): Artist of song that we are trying to match.
        search_results (JSON-format dict): JSON object with list of hits.

    Returns:
        str: "result" field of matching hit in JSON object.

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
    """Get the HTML of the page containing song lyrics from Genius's website.

    Args:
        song_path (str): URL to page with song lyrics

    Returns:
        Response object: page HTML that contains lyrics

    """
    lyrics_url = getGeniusWebsiteBaseURL() + song_path
    page_html = requests.get(lyrics_url)
    return page_html


def parseLyricsPageHTML(html):
    """Extract the lyrics from the song page's HTML."""
    html_text = BeautifulSoup(html.text, "html.parser")
    #  [h.extract() for h in lyrics_html('script')]
    lyrics = html_text.find("div", class_="lyrics").get_text()
    return lyrics
