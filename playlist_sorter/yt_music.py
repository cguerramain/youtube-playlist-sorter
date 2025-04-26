"""Utilities for interacting with the unofficial Youtube Music API."""
import ytmusicapi

from functools import cached_property
from typing import Any, Iterator
from collections.abc import MutableMapping

# Keys in the dict response from `YTMusic.get_playlist()` that do not contain metadata about the playlist.
_NON_METADATA_FIELDS = frozenset(['tracks', 'suggested', 'related'])


def create_client(
  client_id: str, client_secret: str, oauth_json_path: str
) -> ytmusicapi.YTMusic:
  """Returns a client to the unofficial Youtube Music API."""
  credentials = ytmusicapi.OAuthCredentials(client_id, client_secret)
  return ytmusicapi.YTMusic(oauth_json_path, oauth_credentials=credentials)


class Playlist:
  """Represents a Youtube Music playlist to read/modify.

  Attributes:
    client: The `ytmusicapi` client to use.
    playlist_id: The ID of the playlist this class represents.
    playlist_dict: A cached dict with the playlist's information and tracks
        from the unofficial YouTube Music API. See full set of fields at:
        https://ytmusicapi.readthedocs.io/en/stable/reference/playlists.html#ytmusicapi.YTMusic.get_playlist
  """

  def __init__(self, client: ytmusicapi.YTMusic, playlist_id: str):
    self.client = client
    self.playlist_id = playlist_id

  @cached_property
  def playlist_dict(self) -> MutableMapping[str, Any]:
    """Returns a dictionary containing the playlist's information and tracks.

    Returns:
      The entire dict response from:
      https://ytmusicapi.readthedocs.io/en/stable/reference/playlists.html#ytmusicapi.YTMusic.get_playlist
    """
    return self.client.get_playlist(self.playlist_id)

  def metadata(self) -> MutableMapping[str, Any]:
    """Returns a dict with metadata about the playlist."""
    return {
      key: val
      for key, val in self.playlist_dict.items()
      if key not in _NON_METADATA_FIELDS
    }

  def tracks(self) -> Iterator[MutableMapping[str, Any]]:
    """Yields a dict of the next song in the order they appear in the playlist.

    Yields:
      A dict of the next song in the playlist. The dict is an item from the
      "tracks" entry from the below API response, see details at:
      https://ytmusicapi.readthedocs.io/en/stable/reference/playlists.html#ytmusicapi.YTMusic.get_playlist
    """
    yield from self.playlist_dict.get('tracks', [])
