"""
Avik Rao, 08/22/2023
Pulls history from YouTube Music and uses it to scrobble tracks to Last.fm
"""
from ytmusicapi import YTMusic
from pylast import LastFMNetwork
from dataclasses import dataclass
import logging
import time
import json


@dataclass(frozen=True)
class Track:
    title: str
    artist: str
    album: str


class YTMusicScrobbler:
    def __init__(
        self,
        ytm_auth_file: str,
        lastfm_auth_file: str,
        poll_rate: float = 30000,
        logging_level: int = logging.INFO,
    ):
        """
        Class that scrobbles YouTube Music history to Last.fm

        Args:
            ytm_auth_file: Path to JSON file containing YouTube Music OAuth token
            lastfm_auth_file: Path to JSON file containing Last.fm API authentication keys
            poll_rate: Polling rate in milliseconds to YouTube Music API
            logging_level: The [Logging level](https://docs.python.org/3/library/logging.html#logging-levels)
        """

        with open(lastfm_auth_file, "r") as f:
            lastfm_auth_json = json.load(f)
        self.ytmusic_client = YTMusic(ytm_auth_file)
        self.lastfm_client = LastFMNetwork(
            api_key=lastfm_auth_json["API_KEY"],
            api_secret=lastfm_auth_json["SECRET_KEY"],
            username=lastfm_auth_json["USERNAME"],
            password_hash=lastfm_auth_json["PASS_HASH"],
        )
        self.poll_rate = poll_rate / 1000
        self.latest_pulled = None
        self.latest_scrobbled = None

        # Logger configuration
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging_level)
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging_level)
        self.logger.addHandler(console_handler)

    def _get_latest_track(self) -> Track:
        try:
            latest_track = self.ytmusic_client.get_history()[0]
            return Track(
                title=latest_track["title"],
                artist=latest_track["artists"][0]["name"],
                album=latest_track["album"]["name"],
            )
        except Exception as e:
            self.logger.error(e)

    def _scrobble_track(self, track: Track):
        try:
            self.lastfm_client.scrobble(
                artist=track.artist,
                title=track.title,
                album=track.album,
                timestamp=time.time(),
            )
        except Exception as e:
            self.logger.error(e)

    # TODO: Make this async or provide an alternative async method
    def start(self):
        """Start scrobbling tracks to Last.fm"""
        while True:
            self.latest_pulled = self._get_latest_track()
            if self.latest_pulled != self.latest_scrobbled:
                # self._scrobble_track(self.latest_pulled)
                self.logger.info(f"Scrobbled {self.latest_pulled}")
                self.latest_scrobbled = self.latest_pulled
            time.sleep(self.poll_rate)


def main():
    scrobbler = YTMusicScrobbler(
        ytm_auth_file="ytmusic_auth.json", lastfm_auth_file="lastfm_auth.json"
    )
    scrobbler.start()


if __name__ == "__main__":
    main()
