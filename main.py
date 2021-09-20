from ytmusicapi import YTMusic
import pylast
import json
import time

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

    for track in history[:3] :
        print(track)
    
    print()

    with open("last_scrobble.log") as f :
        last_scrobble = [line.strip() for line in f.readlines()[:3]]

    most_recent_track = history[0]
    most_recent = [most_recent_track["title"].strip(), most_recent_track["artist"].strip(), most_recent_track["album"].strip()]

    if most_recent != last_scrobble :
        network.scrobble(title=most_recent[0], artist=most_recent[1], album=most_recent[2], timestamp=time.time())
        with open("last_scrobble.log", "w") as f :
            f.writelines([stat + "\n" for stat in most_recent])
    
    time.sleep(60)



