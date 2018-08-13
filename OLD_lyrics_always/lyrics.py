# GUI for Lyrics Always, using Kivy
# All credit for retrieving song title goes to github.com/XanderMJ

import spotilib
from songinfo import *
import kivy
# import time
# from threading import Thread
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.label import Label

from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.properties import ObjectProperty

from kivy.config import Config
Config.set('graphics', 'borderless', '1')
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 5)
Config.set('graphics', 'top', 200)
Config.set('graphics', 'width', 200)

Builder.load_string('''
<ScrollableLabel>:
    Label:
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        text: root.text
<MainScreen>:
    BoxLayout:
        id: 0
        name: 'layout1'
        orientation: 'vertical'
        Label:
            id: _abc_
            name: 'title_label'
            text: root.title_label_text
            size_hint_y: 0.06
            markup: True
            halign: 'center'
        ScrollableLabel:
            id: _def_
            name: 'lyrics_label'
            text: root.the_lyrics
        Button:
            id: ghi
            name: 'update_lyrics_button'
            text: 'Update'
            size_hint_y: 0.05
            on_press: root.update()

''')

class ScrollableLabel(ScrollView):
    text = StringProperty('')

class MainScreen(BoxLayout):
    the_lyrics = ObjectProperty('Click \'Update\' to find lyrics')
    the_song = ObjectProperty('Update me!')
    pass
    lyrics_text = get_lyrics(spotilib.song_info())
    
    track_information = spotilib.song_info().split(" - ")
    title_label_text = "%s\n\"%s\"" % (track_information[0], track_information[1])
    title_label_text = "[b]%s[/b]" % title_label_text
    
    def update(self):
        track = spotilib.song_info()

        track_information = track.split(" - ")
        title_label_text = "%s\n\"%s\"" % (track_information[0], track_information[1])
        title_label_text = "[b]%s[/b]" % title_label_text


        self.the_lyrics = get_lyrics(track)
        # print "Ouch, that hurt!"
        # return lyrics_text

class ScrollApp(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    ScrollApp().run()
