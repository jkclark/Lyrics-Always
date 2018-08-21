#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
#  import PyQt5.QtWidgets  # was used to redraw GUI (well attempted anyway)
from PyQt5.QtWidgets import (QWidget,
                             QPushButton,
                             #  QHBoxLayout,
                             QVBoxLayout,
                             QApplication,
                             QLabel,
                             QScrollArea,
                             )
from PyQt5 import QtGui, QtCore


class LyricsOverlay(QWidget):

    def __init__(self, lyrics):
        super().__init__()

        self.lyrics = lyrics
        self.lyrics_label = self.createLyricsLabel()

        # this keeps the window on top (I don't know of any side effects yet)
        QtGui.QWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)
        self.initializeUI()

    def initializeUI(self):
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
        self.lyrics = lyrics

    def assembleSongInfoBox(self):
        song_info_box = QVBoxLayout()
        return song_info_box

    def assembleLyricsBox(self):
        #  lyrics_label = self.createLyricsLabel()
        scrolling_lyrics = self.assembleScrollingLyricsWidget(self.lyrics_label)

        lyrics_vertical_box = QVBoxLayout()
        lyrics_vertical_box.addWidget(scrolling_lyrics)
        return lyrics_vertical_box

    # this function is very simple. I don't know if it really makes
    # sense to break it down anymore
    def assembleScrollingLyricsWidget(self, lyrics_label):
        widget = QWidget()  # can change this later to be more specific widget
        widget_vert_layout = QVBoxLayout()
        lyrics_scroll_area = QScrollArea()

        widget_vert_layout.addWidget(lyrics_label)
        widget.setLayout(widget_vert_layout)
        lyrics_scroll_area.setWidget(widget)
        return lyrics_scroll_area

    def createLyricsLabel(self):
        lyrics_label = QLabel(self.lyrics)
        return lyrics_label

    def assembleUpdateButtonBox(self):
        update_button_box = QVBoxLayout()
        update_button = self.createUpdateButton()
        update_button_box.addWidget(update_button)
        return update_button_box

    def createUpdateButton(self):
        update_button = QPushButton("Update", self)
        update_button.setToolTip("Show lyrics for current song")
        update_button.clicked.connect(self.onUpdateButtonClick)
        return update_button

    def onUpdateButtonClick(self):
        #  self.lyrics_label.setText("Here are some new lyrics!")
        #  PyQt5.QtWidgets.qApp.processEvents()
        #  self.lyrics = "Here are some new lyrics"
        self.lyrics_label.setText(self.lyrics)
        #  PyQt5.QtWidgets.qApp.processEvents()


def getInitialPositionCoordinates(app):
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    x = 0
    y = int(rect.height() / 5.0)
    width = 200
    height = 3 * int(rect.height() / 5.0)
    return [x, y, width, height]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    initial_coords_and_dimens = getInitialPositionCoordinates(app)
    temp_lyrics = "Lyrics go here\n\
                   blah blach blacgh blasdkfj dfjdjf"
    lyrics_overlay = LyricsOverlay(temp_lyrics)
    lyrics_overlay.show()
    sys.exit(app.exec_())
