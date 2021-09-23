from ytmusicapi import YTMusic
from datetime import datetime
from pytz import timezone
import pylast
import json
import time

SONGS_TILL_RESET = 5

tz = timezone('US/Eastern')
ytm = YTMusic("headers_auth.json")

with open("lastfm_auth.json", "r") as f :
    lastfm_auth = json.load(f)

API_KEY = lastfm_auth["API_KEY"]
API_SECRET = lastfm_auth["SECRET_KEY"]
USERNAME = lastfm_auth["USERNAME"]
PASS_HASH = lastfm_auth["PASS_HASH"]

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=USERNAME,
    password_hash=PASS_HASH,
)

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



