from requests.packages import urllib3
from ytmusicapi import YTMusic
from datetime import datetime
from pytz import timezone
import pushsafer
import requests
import pylast
import json
import time

SONGS_TILL_RESET = 5
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
default_params = ["" for i in range(13)]

with open("auth.json", "r") as f :
    auth = json.load(f)
    lastfm_auth = auth["lastfm"]
    pushsafer_auth = auth["pushsafer"]

pushsafer.init(pushsafer_auth["API_KEY"])

def main() :

    tz = timezone('US/Eastern')
    ytm = YTMusic("headers_auth.json")

    

    network = pylast.LastFMNetwork(
        api_key=lastfm_auth["API_KEY"],
        api_secret=lastfm_auth["SECRET_KEY"],
        username=lastfm_auth["USERNAME"],
        password_hash=lastfm_auth["PASS_HASH"],
    )

    push_client = pushsafer.Client("", pushsafer_auth["API_KEY"])

    with open("last_scrobble.log", "w") as f :
        pass

    song_counter = 0
    logged_songs = []

    while True :

        if song_counter >= SONGS_TILL_RESET :
            with open("last_scrobble.log", "w") as f :
                song_counter = 1
                logged_songs = [logged_songs[-1]]

        raw_history = ytm.get_history()[:5]
        history = [{"title": song["title"], "artist": song["artists"][0]["name"], "album": song["album"]["name"] } for song in raw_history]

        print(datetime.now(tz))
        most_recent_track = history[0]
        most_recent = [most_recent_track["title"].strip(), most_recent_track["artist"].strip(), most_recent_track["album"].strip()]
        print(most_recent)

        if not most_recent in logged_songs :
            print("New song scrobbled!")
            network.scrobble(title=most_recent[0], artist=most_recent[1], album=most_recent[2], timestamp=time.time())
            logged_songs.append(most_recent)
            song_counter += 1
            with open("last_scrobble.log", "a") as f :
                f.writelines([stat + "\n" for stat in most_recent])
                f.write("\n")
        
        print()
        time.sleep(60)

try :
    main()
except KeyboardInterrupt: 
    pushsafer.Client("").send_message("Script voluntarily stopped (KeyboardInterrupt)", "YTMScrobbler Error", pushsafer_auth["DEVICE_ID"], *default_params)
    exit(0)
except Exception as e:
    error = getattr(e, 'message', repr(e))
    print(error)
    pushsafer.Client("").send_message(error, "YTMScrobbler Error", pushsafer_auth["DEVICE_ID"], *default_params)



