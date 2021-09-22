from ytmusicapi import YTMusic
from datetime import datetime
from pytz import timezone
import pylast
import json
import time

tz = timezone('US/Eastern')
ytm = YTMusic("headers_auth.json")

with open("lastfm_auth.json", "r") as f :
    lastfm_auth = json.load(f)

API_KEY = lastfm_auth["API_KEY"]
API_SECRET = lastfm_auth["SECRET_KEY"]
USERNAME = lastfm_auth["USERNAME"]
PASS_HASH = pylast.md5(lastfm_auth["PASSWORD"])

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=USERNAME,
    password_hash=PASS_HASH,
)

while True :

    raw_history = ytm.get_history()[:5]
    history = [{"title": song["title"], "artist": song["artists"][0]["name"], "album": song["album"]["name"] } for song in raw_history]

    print(datetime.now(tz))
    for track in history[:3] :
        print(track)

    with open("last_scrobble.log") as f :
        lines = f.readlines()
        last_three = [[line.strip() for line in lines[i*4 : (i*4) + 3]] for i in range(3)]

    most_recent_track = history[0]
    most_recent = [most_recent_track["title"].strip(), most_recent_track["artist"].strip(), most_recent_track["album"].strip()]
    print(most_recent)

    if not most_recent in last_three :
        print("New song scrobbled!")
        network.scrobble(title=most_recent[0], artist=most_recent[1], album=most_recent[2], timestamp=time.time())
        with open("last_scrobble.log", "w") as f :
            f.writelines([stat + "\n" for stat in most_recent])
    
    print()
    
    time.sleep(60)



