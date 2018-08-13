import sys
import spotipy
import spotipy.util as util
import json

scope = 'user-read-currently-playing'

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print "Usage: %s username" % (sys.argv[0],)
    sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.current_user_playing_track()
    print "### results ###"
    parsed = json.loads(str(results))
    print json.dumps(parsed, indent=4, sort_keys=True)
else:
    print "Can't get token for", username
