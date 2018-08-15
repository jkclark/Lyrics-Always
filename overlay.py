#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget,
                             QPushButton,
                             #  QHBoxLayout,
                             QVBoxLayout,
                             QApplication,
                             QLabel,
                             QScrollArea,
                             )


class LyricsOverlay(QWidget):

    def __init__(self, lyrics):
        super().__init__()

        self.lyrics = lyrics

        self.initializeUI()

    def initializeUI(self):
        main_vertical_box = QVBoxLayout()

        song_info_box = self.assembleSongInfoBox()
        lyrics_box = self.assembleLyricsBox()
        update_button_box = self.assembleUpdateButtonBox()

        main_vertical_box.addLayout(song_info_box)
        main_vertical_box.addLayout(lyrics_box)
        main_vertical_box.addLayout(update_button_box)

        init_x, init_y, init_w, init_h = initial_coords_and_dimens
        self.setGeometry(init_x, init_y, init_w, init_h)
        self.setLayout(main_vertical_box)
        self.setWindowTitle('Lyrics Always')
        self.show()

    def assembleSongInfoBox(self):
        song_info_box = QVBoxLayout()
        return song_info_box

    def assembleLyricsBox(self):
        lyrics_label = self.createLyricsLabel()
        scrolling_lyrics = self.assembleScrollingLyricsWidget(lyrics_label)

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
        update_button = QPushButton("Update")
        return update_button


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
    temp_lyrics = "\t\t\tLyrics go here\n\
                    hello my name is josh\n\
                    yesterday i went to the gym\n\
                    jason is raging about demon souls\n\
                    i am trying to make some text\n\
                    that resembles lyrics\n\
                    and see how it shows up in the window\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf\n\
                    blah blach blacgh blasdkfj dfjdjf"
    lyrics_overlay = LyricsOverlay(temp_lyrics)
    sys.exit(app.exec_())
