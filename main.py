"""
Entrypoint script to start scrobbling YouTube Music history to Last.FM
Avik Rao, 08/23/2023
"""
from YTMusicScrobbler import YTMusicScrobbler

YTM_AUTH_FILE = "ytmusic_auth.json"
LFM_AUTH_FILE = "lastfm_auth.json"


def main():
    scrobbler = YTMusicScrobbler(
        ytm_auth_file=YTM_AUTH_FILE, lastfm_auth_file=LFM_AUTH_FILE
    )
    scrobbler.start()


if __name__ == "__main__":
    main()
