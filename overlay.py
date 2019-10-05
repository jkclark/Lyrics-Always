#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Most of the functions in this module create parts of the GUI."""

from PyQt5.QtWidgets import (QWidget,
                             QPushButton,
                             QVBoxLayout,
                             QLabel,
                             QScrollArea,
                             )
from PyQt5 import QtGui, QtCore


class LyricsLabel(QLabel):

    def __init__(self, lyrics):
        QLabel.__init__(self, lyrics)


class LyricsOverlay(QWidget):
    """Overlay widget that displays song title, artist, and lyrics.

    Attributes:
        title (str): Title of the current song.
        artist (str): Artist of the current song.
        lyrics (str): Lyrics for the current song.

    """

    def __init__(self, title, artist, lyrics):
        super().__init__()

        self.title = title
        self.artist = artist
        self.current_song = self.createFullSongName(title, artist)
        self.song_label = self.createSongLabel()

        self.lyrics = lyrics
        self.lyrics_label = self.createLyricsLabel()
        self.lyrics_scroll_area = None  # gets set during initializeUI()

        # The line below makes the label stay as wide as the longest line
        # (i.e., text does not wrap)
        #  self.lyrics_label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        # This keeps the window on top (I haven't noticed  any side effects yet)
        # use '|' to specify multiple flags
        QtGui.QWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.initializeUI()

    def initializeUI(self):
        """Dynamically create all the parts of the GUI."""
        main_vertical_box = QVBoxLayout()

        song_info_box = self.assembleSongInfoBox()
        lyrics_box = self.assembleLyricsBox()
        update_button_box = self.assembleUpdateButtonBox()

        main_vertical_box.addLayout(song_info_box)
        main_vertical_box.addLayout(lyrics_box)
        main_vertical_box.addLayout(update_button_box)

        #  init_x, init_y, init_w, init_h = initial_coords_and_dimens
        #  self.setGeometry(init_x, init_y, init_w, init_h)
        self.setLayout(main_vertical_box)
        self.setWindowTitle('Lyrics Always')
        #  self.show()

    def setLyrics(self, lyrics):
        """ Set lyrics and update lyrics label """
        self.lyrics = lyrics
        self.lyrics_label.setText(self.lyrics)

    def createFullSongName(self, title, artist):
        return artist + " - " + title

    def getCurrentSong(self):
        return self.current_song

    def didSongChange(self, new_title, new_artist):
        """Check to see if 'new' song is different from current song.

        Args:
            new_title (str): Title of song to be compared with current song.
            new_artist (str): Artist of song to be compared with current song.

        Returns:
            True if song is different from current song, False otherwise.

        """
        new_song = self.createFullSongName(new_title, new_artist)
        if self.current_song == new_song:
            return False
        return True

    def setCurrentSong(self, new_title, new_artist):
        """ Set current_song and update song label """
        self.current_song = self.createFullSongName(new_title, new_artist)
        self.song_label.setText(self.current_song)

    # UI Components #
    def assembleSongInfoBox(self):
        """Create part(s) of the GUI."""
        song_info_box = QVBoxLayout()
        song_info_box.addWidget(self.song_label)
        return song_info_box

    def createSongLabel(self):
        """Create part(s) of the GUI."""
        song_label = QLabel(self.current_song)
        song_label.setWordWrap(True)
        return song_label

    def updateSongLabel(self):
        self.song_label.setText(self.current_song)

    def assembleLyricsBox(self):
        """Create part(s) of the GUI."""
        #  lyrics_label = self.createLyricsLabel()
        scrolling_lyrics = self.assembleScrollingLyricsWidget(self.lyrics_label)

        lyrics_vertical_box = QVBoxLayout()
        lyrics_vertical_box.addWidget(scrolling_lyrics)
        return lyrics_vertical_box

    # This function is already very simple. I don't know if it really makes
    # sense to break it down any more
    def assembleScrollingLyricsWidget(self, lyrics_label):
        """Create part(s) of the GUI."""
        widget = QWidget()  # can change this later to be more specific widget
        widget_vert_layout = QVBoxLayout()
        lyrics_scroll_area = QScrollArea()
        lyrics_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        lyrics_scroll_area.setWidgetResizable(True)  # fixes part of issue #9

        widget_vert_layout.addWidget(lyrics_label)
        widget.setLayout(widget_vert_layout)
        lyrics_scroll_area.setWidget(widget)

        self.lyrics_scroll_area = lyrics_scroll_area
        return lyrics_scroll_area

    def createLyricsLabel(self):
        """Create part(s) of the GUI."""
        lyrics_label = LyricsLabel(self.lyrics)
        lyrics_label.setWordWrap(True)
        return lyrics_label

    def assembleUpdateButtonBox(self):
        """Create part(s) of the GUI."""
        update_button_box = QVBoxLayout()
        update_button = self.createUpdateButton()
        update_button_box.addWidget(update_button)
        return update_button_box

    def createUpdateButton(self):
        """Create part(s) of the GUI."""
        update_button = QPushButton("Update", self)
        update_button.setToolTip("Show lyrics for current song")
        return update_button

    def _scrollToTop(self):
        """Reset the view of the lyrics area to the top."""
        self.lyrics_scroll_area.verticalScrollBar().setValue(0)
