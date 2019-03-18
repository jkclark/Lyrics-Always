import overlay
import getSongInfoFromSpotify as spotify
import getLyricsFromGenius as genius

from PyQt5.QtWidgets import (QApplication,
                             QPushButton)
#  from PyQt5.QtCore import Qt  # imported for color
#  from PyQt5 import QtGui
import qdarkstyle

import sys


class User():
    """Object to keep track of Spotify API credentials, scope, and token.

    Attributes:
        username (str): Spotify username of user.
        scope (str): The scope we have access to for the user.
        credentials_dict (dict of str: str): API info (token, keys, etc).

    """

    def __init__(self, username, scope, credentials_dict):
        self.username = username
        self.scope = scope
        self.credentials_dict = credentials_dict

        #: str: access token for user
        self.token = self.requestToken()

    def getUsername(self):
        return self.username

    def getScope(self):
        return self.scope

    def getCredentialsDict(self):
        return self.credentials_dict

    def requestToken(self):
        """Get a token to authorize Spotify API use for this user."""
        token = spotify.get_user_token(
                    self.username,
                    self.scope,
                    self.credentials_dict,
                )
        return token

    def getToken(self):
        return self.token


def getInitialPositionCoordinates(app):
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    x = 0
    y = int(rect.height() / 5.0)
    width = 200
    height = 3 * int(rect.height() / 5.0)
    return [x, y, width, height]


def checkResponseStatus(response_json):
    status = response_json["meta"]["status"]
    return status


def getSongFromSpotify(user):
    """Get information (title and artist) about currently playing Spotify song.

    Args:
        user (User): User object with information about Spotify credentials.

    Returns:
        song_title (str): The name of song currently playing on Spotify.
        song_artist (str): The artist of song currently playing on Spotify.

    """
    playback_info_json = spotify.get_current_playback_info_json(user.token)

    song_title = spotify.getSongTitleFromPlaybackObj(playback_info_json)
    song_artist = spotify.getSongArtistFromPlaybackObj(playback_info_json)
    return song_title, song_artist


def getLyricsForSong(song_title, song_artist):
    search_urls = genius.createSearchGETRequestURLs(song_title, song_artist)
    matching_hit = None
    for url in search_urls:
        response_json = genius.searchGenius(url)
        status = checkResponseStatus(response_json)
        if status != 200:
            error_message = "Failed to get lyrics. Search returned status {}."
            error_message = error_message.format(status)
            return error_message

        matching_hit = genius.findMatchingHitInSearchResults(song_title,
                                                             song_artist,
                                                             response_json)

        if matching_hit is not None:
            print("Successful URL: ", url)
            break

    if matching_hit is None:  # Can't find a song page for this song
        no_lyrics_text = "Cannot find lyrics for current song."
        return no_lyrics_text

    song_path = genius.extractSongPathFromGeniusSearchResult(matching_hit)
    lyrics_page_html = genius.getLyricsPageHTMLFromPath(song_path)
    lyrics = genius.parseLyricsPageHTML(lyrics_page_html)
    lyrics = lyrics.strip()  # Remove beginning and ending newlines
    return lyrics


def update(user, la, app):
    title, artist = getSongFromSpotify(user)
    if la.didSongChange(title, artist):
        la.setCurrentSong(title, artist)
        lyrics = getLyricsForSong(title, artist)
        la.setLyrics(lyrics)
        print("Song updated: ", la.getCurrentSong())
        app.processEvents()
        la._scrollToTop()


def main():
    # get user creds
    spotify.check_args()
    username = spotify.get_username()
    scope = spotify.get_scope()
    credentials_pickle_file = "credentials.p"
    credentials_dict = spotify.load_credentials(credentials_pickle_file)
    user = User(username, scope, credentials_dict)

    title, artist = getSongFromSpotify(user)
    lyrics = getLyricsForSong(title, artist)

    # make app with lyrics
    app = QApplication(sys.argv)
    initial_coords_and_dimens = getInitialPositionCoordinates(app)
    x, y, w, h = initial_coords_and_dimens

    lyrics_overlay = overlay.LyricsOverlay(title, artist, lyrics)
    lyrics_overlay.setGeometry(x, y, w, h)

    push_button_child = lyrics_overlay.findChild(QPushButton)
    push_button_child.clicked.connect(lambda: update(user,
                                                     lyrics_overlay,
                                                     app))

    # change color of entire window
    lyrics_overlay.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    lyrics_overlay.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
