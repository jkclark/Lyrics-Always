#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QWidget,
                             QPushButton,
                             #  QHBoxLayout,
                             QVBoxLayout,
                             QApplication,
                             )


class LyricsOverlay(QWidget):

    def __init__(self):
        super().__init__()

        self.initializeUI()

    def initializeUI(self):
        main_vertical_box = QVBoxLayout()

        song_info_box = self.createSongInfoBox()
        lyrics_box = self.createLyricsBox()
        update_button_box = self.createUpdateButtonBox()

        main_vertical_box.addLayout(song_info_box)
        main_vertical_box.addLayout(lyrics_box)
        main_vertical_box.addLayout(update_button_box)

        init_x, init_y, init_w, init_h = initial_coords_and_dimens
        self.setGeometry(init_x, init_y, init_w, init_h)
        self.setLayout(main_vertical_box)
        self.setWindowTitle('Lyrics Always')
        self.show()

    def createSongInfoBox(self):
        song_info_box = QVBoxLayout()
        return song_info_box

    def createLyricsBox(self):
        lyrics_box = QVBoxLayout()
        return lyrics_box

    def createUpdateButtonBox(self):
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
    lyrics_overlay = LyricsOverlay()
    sys.exit(app.exec_())
