# Lyrics Always: Lyrics for Spotify

__Edit 8/8/2018__: I am in the process of recreating Lyrics Always. Not only is the existing code hideous, but also Lyrics Always is aesthetically displeasing and only works for Windows. I am redesigning it for Windows, Mac, and Linux, as well as rewriting and refactoring the code. You can find the old code in OLD\_lyrics\_always/.

---

## Intro
Hi! I hope you're having a good day. I don't know about you, but I really like to
sing the words to songs that I like. Nailing all of the words to Kendrick Lamar's "m.A.A.d city"
perfeclty in sync with him is a great feeling. I also (used to) play a lot of Hearthstone, a virtual card game
that involves taking turns. Half of the time that you're playing, however, it's your opponent's turn, leaving you
with nothing to do (strategically, you should being paying attention to what your opponent is doing, but it's a pretty passive
75 seconds). I want to learn the words to a lot of songs, and I figure that my opponent's turn in Hearthstone
is a great time to do that. That's why I decided to write Lyrics Always.

## What does Lyrics Always do?
Lyrics Always brings up a little overlay, displaying the lyrics to the song currently playing in the Spotify for Windows Desktop app, in addition
to the song's name and artist. The button underneath the lyrics updates the lyrics to match the song that is currently playing.
That's all there is to it.

## What you need
Here are the dependencies you need to get Lyrics Always up and running:

* Kivy 1.10.0+
* BeautifulSoup 4

## Credit where credit is due
Credit for fetching the song title and artist from the Spotify app goes to github.com/XanderMJ. I used his/her code which can be
found at https://github.com/XanderMJ/spotilib.

## Usage
You can run Lyrics Always by navigating to it's directory and running `python lyrics.py`

Enjoy!
