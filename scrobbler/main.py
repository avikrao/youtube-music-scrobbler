from requests.packages import urllib3
from ytmusicapi import YTMusic
import pylast
import json
import time
import os 

PING_FILE = "/data/pinglog.txt"
LOG_FILE = "/data/scrobblelog.json"
LOG_LENGTH = 20
SONGS_TILL_RESET = 5

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
default_params = ["" for i in range(13)]

with open("auth.json", "r") as f :
    auth = json.load(f)
    lastfm_auth = auth["lastfm"]

def main(logs) :

    ytm = YTMusic("headers_auth.json")

    network = pylast.LastFMNetwork(
        api_key=lastfm_auth["API_KEY"],
        api_secret=lastfm_auth["SECRET_KEY"],
        username=lastfm_auth["USERNAME"],
        password_hash=lastfm_auth["PASS_HASH"],
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

        raw_history = ytm.get_history()[0]
        
        timestamp = str(time.time())

        if not raw_history or not raw_history["title"] or not raw_history["artists"] or not raw_history["album"] :
            continue
        
        most_recent_track = {"title": raw_history["title"], "artist": raw_history["artists"][0]["name"], "album": raw_history["album"]["name"]}
        most_recent = [most_recent_track["title"].strip(), most_recent_track["artist"].strip(), most_recent_track["album"].strip()]
        print(timestamp)
        print(most_recent_track)

        if most_recent:
            new_entry = {
                "timestamp": timestamp,
                "title": most_recent[0],
                "artist": most_recent[1],
                "album": most_recent[2]
            }
        else:
            new_entry = {
                "timestamp": timestamp,
                "error": True
            }

        if not most_recent in logged_songs :
            print("New song scrobbled!")
            network.scrobble(title=most_recent[0], artist=most_recent[1], album=most_recent[2], timestamp=time.time())
            logged_songs.append(most_recent)
            song_counter += 1

            with open("last_scrobble.log", "a") as f :
                f.writelines([stat + "\n" for stat in most_recent])
                f.write("\n")

            logs.append(new_entry)
            if len(logs) > LOG_LENGTH:
                logs[:] = logs[(len(logs)-LOG_LENGTH):]
            
            with open(LOG_FILE, "w") as f:
                json.dump(logs, f, indent=2)
        
        with open(PING_FILE, "w") as f:
            f.write(str(time.time()))

        print()
        time.sleep(60)

if __name__ == '__main__':

    if not os.path.exists(LOG_FILE):
        logs = []
    else:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)

    try:
        main(logs)
    except:
        timestamp = str(time.time())
        logs.append({"timestamp": timestamp, "error": True})

        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=2)



