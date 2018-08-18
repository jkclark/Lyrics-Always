import sys
import spotipy
import spotipy.util as util
import pickle
import json


def check_args():
    if len(sys.argv) != 2:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit(1)


def get_username():
    return sys.argv[1]


def get_scope():
    #  return "user-read-currently-playing"
    return "user-read-playback-state"


def load_credentials(credentials_pickle_file):
    try:
        with open(credentials_pickle_file, 'rb') as c:
            return pickle.load(c)
    except IOError:
        print("Error: Couldn't open credentials file. Exiting.")
        sys.exit(1)


def get_user_token(username, scope, credentials_dict):
    token = util.prompt_for_user_token(
            username,
            scope,
            client_id=credentials_dict['SPOTIPY_CLIENT_ID'],
            client_secret=credentials_dict['SPOTIPY_CLIENT_SECRET'],
            redirect_uri=credentials_dict['SPOTIPY_REDIRECT_URI'],
            )
    if token is None:
        print("Error: Can't get token for", username)
        sys.exit(1)
    return token


def get_current_playback_info_json(token):
    sp = spotipy.Spotify(auth=token)
    #  results = sp.current_user_playing_track()
    results = sp.current_playback()
    return results


def load_json_into_object(unparsed_json):
    json_string = json.dumps(unparsed_json)
    json_obj = json.loads(json_string)
    return json_obj


def getSongTitleFromPlaybackObj(playback_obj):
    return playback_obj["item"]["name"]


def getSongArtistFromPlaybackObj(playback_obj):
    primary_artist = playback_obj["item"]["artists"][0]
    return primary_artist["name"]


def main():
    check_args()
    print("Retrieving song info from Spotify")
    username = get_username()
    scope = get_scope()
    credentials_pickle_file = "credentials.p"
    credentials_dict = load_credentials(credentials_pickle_file)
    token = get_user_token(username, scope, credentials_dict)
    unparsed_playback_info_json = get_current_playback_info_json(token)
    current_playback_obj = load_json_into_object(unparsed_playback_info_json)
    song_title = getSongTitleFromPlaybackObj(current_playback_obj)
    print("current song title:", song_title)
    song_artist = getSongArtistFromPlaybackObj(current_playback_obj)
    print("current song artist:", song_artist)


if __name__ == "__main__":
    main()
