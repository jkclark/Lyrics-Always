import sys
import spotipy
import spotipy.util as util
import pickle


def check_args():
    """Make sure that the program is invoked correctly.

    The program should be called by it's name, followed by a Spotify username.
    """
    if len(sys.argv) != 2:
        print("Usage: %s username" % (sys.argv[0],))
        sys.exit(1)


def get_username():
    return sys.argv[1]


def get_scope():
    # user-read-playback-state gives access to user's currently playing track.
    return "user-read-playback-state"


def load_credentials(credentials_pickle_file):
    """Get the Spotify API credentials by loading a pickle file.

    Args:
        credentials_pickle_file (str): Path to pickle file containing creds.

    Returns:
        dict: dictionary containing API keys, redirect URI, etc.

    """
    try:
        with open(credentials_pickle_file, 'rb') as c:
            return pickle.load(c)
    except IOError:
        print("Error: Couldn't open credentials file. Exiting.")
        sys.exit(1)


def get_user_token(username, scope, credentials_dict):
    """Get a token to authorize Spotify API use for user.

    Documenation for this Spotipy.util function is available here:
    https://spotipy.readthedocs.io/en/latest/?highlight=prompt%20user%20token#
    spotipy.util.prompt_for_user_token

    Args:
        username (str): username of Spotify account for which to get token.
        scope (str): scope of authorization for Spotify token.
        credentials_dict (dict of str: str): API keys and redirect URI
    """
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
    """Get unparsed playback information in JSON format, authorized by token.

    Args:
        token: Spotify token to authorize requests for user playback info.

    Returns:
        JSON object (dict): JSON-format dictionary of playback info

    """
    sp = spotipy.Spotify(auth=token)
    #  results = sp.current_user_playing_track()
    results = sp.current_playback()
    print(f"Results: {results}")
    return results


def getSongTitleFromPlaybackObj(playback_obj):
    """Return the name of the song (str) from the JSON dictionary."""
    return playback_obj["item"]["name"]


def getSongArtistFromPlaybackObj(playback_obj):
    """Return the artist of the song (str) from the JSON dictionary."""
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
    song_title = getSongTitleFromPlaybackObj(unparsed_playback_info_json)
    print("current song title:", song_title)
    song_artist = getSongArtistFromPlaybackObj(unparsed_playback_info_json)
    print("current song artist:", song_artist)


if __name__ == "__main__":
    main()
