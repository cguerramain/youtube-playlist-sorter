"""Script to sort a given Youtube Music playlist.

Usage (run from the base repo directory):
  python3 -m playlist_sorter.sort_playlist_main
"""

import os
import sys

from datetime import datetime
from dotenv import load_dotenv
from playlist_sorter import yt_music

load_dotenv()
OAUTH_JSON_PATH = os.getenv('OAUTH_JSON_PATH')
GCP_CLIENT_ID = os.getenv('GCP_CLIENT_ID')
GCP_CLIENT_SECRET = os.getenv('GCP_CLIENT_SECRET')
DEFAULT_PLAYLIST_ID = os.getenv('DEFAULT_PLAYLIST_ID')
DEFAULT_OUTPUT_DIR = os.getenv('DEFAULT_OUTPUT_DIR')

if __name__ == '__main__':
  client = yt_music.create_client(
    GCP_CLIENT_ID, GCP_CLIENT_SECRET, OAUTH_JSON_PATH
  )
  playlist = yt_music.Playlist(client, DEFAULT_PLAYLIST_ID)

  if DEFAULT_OUTPUT_DIR:
    now = datetime.now()
    seconds_today = now.hour * 3600 + now.minute * 60 + now.second
    title = playlist.metadata()['title']
    filename = f'{title}_{now.strftime("%Y%m%d")}_{seconds_today:05d}.csv'
    path_or_buf = os.path.join(DEFAULT_OUTPUT_DIR, filename)
  else:
    path_or_buf = sys.stdout
  playlist.to_csv(path_or_buf)
