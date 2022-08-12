from typing import Optional

from api.lookup.util import convert_to_date, fetch_data, sanitize


class MusicLookup:
    base_url = 'https://api.deezer.com/'

    @classmethod
    def lookup_by_deezer_id(
        cls, deezer_id: int, media_type: str
    ) -> dict | None:
        """Retrieves music data with the given deezer id.

        Args:
            deezer_id (int): Deezer id to lookup with.
            media_type (str): Music type - (Song or Album)

        Returns:
            dict | None: Music with deezer id if found else None
        """
        if media_type == 'album':
            url = f'{cls.base_url}/album/{deezer_id}'
        else:
            url = f'{cls.base_url}/track/{deezer_id}'

        json_values = fetch_data(sanitize(url))

        music = None
        if json_values:
            if media_type == 'album':
                music = cls._parse_album_data(json_values)
            else:
                music = cls._parse_track_data(json_values)
        return music

    @classmethod
    def search_for_track(
        cls,
        title: str,
        artist: Optional[str] = None,
        album: Optional[str] = None,
    ) -> list[dict]:
        """Retrieves list of all songs with given title,
        can optionally filter list by album and artist.

        Args:
            title (str): Track title to search for
            artist (:obj:'str', optional): Artist to filter search with
            album (:obj:'str', optional): Album to filter search with

        Returns:
            list[dict]: Tracks found in search
        """
        url = f'{cls.base_url}/search/track?q="{title}"'

        if artist:
            url += f' artist:"{artist}"'
        if album:
            url += f' album:"{album}"'

        json_values = fetch_data(sanitize(url))

        track_list = []

        if json_values:
            for track in json_values['data']:
                track_list.append(cls._parse_track_data(track, json=True))

        return track_list

    @classmethod
    def search_for_album(
        cls, album: str, artist: Optional[str] = None
    ) -> list[dict]:
        """Retrieves list of all albums with the given title,
        can optionally filter by artist.

        Args:
            album (str): Album title to search for
            artist (:obj:'str', optional): Artist to filter search with

        Returns:
            list[dict]: Albums found in search
        """
        url = f'{cls.base_url}/search/album?q="{album}"'

        if artist:
            url += f' artist:"{artist}"'

        json_values = fetch_data(sanitize(url))

        album_list = []
        if json_values:
            for album in json_values['data']:
                album_list.append(cls._parse_album_data(album))
        return album_list

    @classmethod
    def search_for_artist(cls, artist: str) -> list[dict]:
        """Retrieves all tracks by the given artist

        Args:
            artist (str): Artist to search with

        Returns:
            list[dict]: Tracks found in search
        """
        url = f'{cls.base_url}/search/track?q=artist:"{artist}"'

        json_values = fetch_data(sanitize(url))

        track_list = []
        if json_values:
            for track in json_values['data']:
                track_list.append(cls._parse_track_data(track, json=True))
        return track_list

    @classmethod
    def _parse_track_data(
        cls, music_data: dict, json: Optional[bool] = False
    ) -> dict:
        """Parses response sdata for relevant track information.

        Args:
            music_data (dict): Response data to parse
            json (:obj:'bool', optional): if True return in json
                compatible format

        Returns:
            dict: parsed response data
        """
        artist_data = music_data.get('artist')
        album_data = music_data.get('album')

        release_date = music_data.get('release_date')
        release_date = release_date if json else convert_to_date(release_date)

        return {
            'track': music_data.get('title'),
            'release_date': release_date,
            'artist': artist_data.get('name'),
            'album': album_data.get('title'),
            'deezer_id': music_data.get('id'),
            'music_type': music_data.get('type'),
            'cover': album_data.get('cover_medium'),
        }

    @classmethod
    def _parse_album_data(cls, album_data: dict) -> dict:
        """Parses response sdata for relevant album information.

        Args:
            album_data (dict): Response data to parse

        Returns:
            dict: parsed response data
        """
        artist_data = album_data.get('artist')

        return {
            'track': None,
            'release_date': None,
            'artist': artist_data.get('name'),
            'album': album_data.get('title'),
            'deezer_id': album_data.get('id'),
            'music_type': album_data.get('type'),
            'cover': album_data.get('cover_medium'),
        }
