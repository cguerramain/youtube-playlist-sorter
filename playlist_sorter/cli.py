"""Script to sort a given Youtube Music playlist.

Usage (run from the base repo directory):
  python3 -m playlist_sorter.cli playlist ls --help
"""

import sys
import typer
import dataclasses
import ytmusicapi
import json
from functools import cached_property
import pathlib

from typing_extensions import Annotated
from datetime import datetime
from dotenv import load_dotenv
from playlist_sorter import yt_music

load_dotenv()

app = typer.Typer(name='yt_cli')
playlist_app = typer.Typer()
app.add_typer(playlist_app, name='playlist')


@dataclasses.dataclass
class AppState:
  """Holds common flags, eg. GCP credentials."""

  gcp_client_id: str = ''
  gcp_client_secret_key: str = ''
  oauth_json_path: str = ''

  @cached_property
  def client(self) -> ytmusicapi.YTMusic:
    return yt_music.create_client(
      self.gcp_client_id, self.gcp_client_secret_key, self.oauth_json_path
    )


app_state = AppState()


@app.callback()
def main(
  gcp_client_id: Annotated[
    str, typer.Option(envvar='GCP_CLIENT_ID', help='GCP client ID.')
  ],
  gcp_client_secret_key: Annotated[
    str, typer.Option(envvar='GCP_CLIENT_SECRET', help='GCP client secret key.')
  ],
  oauth_json_path: Annotated[
    str, typer.Option(envvar='OAUTH_JSON_PATH', help='OAuth JSON path.')
  ],
):
  global app_state
  app_state = AppState(
    gcp_client_id=gcp_client_id,
    gcp_client_secret_key=gcp_client_secret_key,
    oauth_json_path=oauth_json_path,
  )


PlaylistIdArg = Annotated[
  str, typer.Option(envvar='PLAYLIST_ID', help='The ID of the playlist.')
]


@playlist_app.command('ls')
def playlist_ls(playlist_id: PlaylistIdArg = ''):
  playlist = yt_music.Playlist(app_state.client, playlist_id)
  typer.echo(json.dumps(playlist.playlist_dict, indent=2))


@playlist_app.command('to_csv')
def playlist_to_csv(
  playlist_id: PlaylistIdArg,
  output_path: Annotated[
    str,
    typer.Option(
      envvar='DEFAULT_OUTPUT_DIR',
      help=(
        'The path of a file or diretory to write to. If empty, writes to '
        'stdout.'
      ),
    ),
  ],
):
  playlist = yt_music.Playlist(app_state.client, playlist_id)
  if not output_path:
    playlist.to_csv(sys.stdout)
    return

  output_path = pathlib.Path(output_path)
  if output_path.is_dir():
    now = datetime.now()
    seconds_today = now.hour * 3600 + now.minute * 60 + now.second
    title = playlist.metadata()['title']
    filename = f'{title}_{now.strftime("%Y%m%d")}_{seconds_today:05d}.csv'
    full_path = output_path / filename
  else:
    full_path = output_path
  playlist.to_csv(full_path)


if __name__ == '__main__':
  app()
