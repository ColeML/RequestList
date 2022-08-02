from datetime import date
from api.lookup.util import fetch_data, sanitize
from typing import Optional


class MusicLookup:
    base_url = "https://api.deezer.com/"

    @classmethod
    def lookup_by_deezer_id(cls, deezer_id: int, media_type: str) -> dict | None:
        if media_type == 'album':
            url = f"{cls.base_url}/album/{deezer_id}"
        else:
            url = f"{cls.base_url}/track/{deezer_id}"

        json_values = fetch_data(sanitize(url))

        if json_values:
            if media_type == 'album':
                return cls._parse_album_data(json_values)
            return cls._parse_track_data(json_values)

    @classmethod
    def search_for_track(cls, title: str, artist: Optional[str] = None, album: Optional[str] = None) -> list[dict]:
        url = f"{cls.base_url}/search/track?q=\"{title}\""

        if artist:
            url += f" artist:\"{artist}\""
        if album:
            url += f" album:\"{album}\""

        json_values = fetch_data(sanitize(url))

        track_list = []

        if json_values:
            for track in json_values["data"]:
                track_list.append(cls._parse_track_data(track))

        return track_list

    @classmethod
    def search_for_album(cls, album: str, artist: Optional[str] = None) -> list[dict]:
        url = f"{cls.base_url}/search/album?q=\"{album}\""

        if artist:
            url += f" artist:\"{artist}\""

        json_values = fetch_data(sanitize(url))

        album_list = []

        if json_values:
            for album in json_values["data"]:
                album_list.append(cls._parse_album_data(album))

        return album_list

    @classmethod
    def search_for_artist(cls, artist: str) -> list[dict]:
        url = f"{cls.base_url}/search/track?q=artist:\"{artist}\""

        json_values = fetch_data(sanitize(url))

        track_list = []
        if json_values:
            for track in json_values["data"]:
                track_list.append(cls._parse_track_data(track))

        return track_list

    @classmethod
    def _parse_track_data(cls, music_data: dict) -> dict:
        artist_data = music_data.get('artist')
        album_data = music_data.get('album')

        return {
            "track": music_data.get("title"),
            "release_date": cls._convert_to_date(music_data.get("release_date")),
            "artist": artist_data.get('name'),
            "album": album_data.get('title'),
            "deezer_id": music_data.get("id"),
            "music_type": music_data.get('type'),
            "cover": album_data.get('cover_medium')
        }

    @classmethod
    def _parse_album_data(cls, album_data: dict) -> dict:
        artist_data = album_data.get('artist')

        return {
            "track": None,
            "release_date": None,
            "artist": artist_data.get("name"),
            "album": album_data.get('title'),
            "deezer_id": album_data.get("id"),
            "music_type": album_data.get('type'),
            "cover": album_data.get('cover_medium')
        }

    @classmethod
    def _convert_to_date(cls, _date) -> date | None:
        if _date:
            return date.fromisoformat(_date)
