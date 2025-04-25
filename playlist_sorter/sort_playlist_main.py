"""Script to sort a given Youtube Music playlist.

Usage (run from the base repo directory):
  python3 -m playlist_sorter.sort_playlist_main
"""

import os
import json
from playlist_sorter import yt_music

from dotenv import load_dotenv

load_dotenv()
OAUTH_JSON_PATH = os.getenv('OAUTH_JSON_PATH')
GCP_CLIENT_ID = os.getenv('GCP_CLIENT_ID')
GCP_CLIENT_SECRET = os.getenv('GCP_CLIENT_SECRET')
DEFAULT_PLAYLIST_ID = os.getenv('DEFAULT_PLAYLIST_ID')

if __name__ == '__main__':
  client = yt_music.create_client(
    GCP_CLIENT_ID, GCP_CLIENT_SECRET, OAUTH_JSON_PATH
  )
  playlist = yt_music.Playlist(client, DEFAULT_PLAYLIST_ID)
  for track in playlist.tracks():
    print(json.dumps(track, indent=2))
