import os

from api.lookup.util import fetch_data


class VideoLookup:
    base_url = 'http://www.omdbapi.com'
    api_key = os.environ.get('OMDB_API_KEY')

    @classmethod
    def search_by_title_year(
        cls, title: str, year: int, _type: str
    ) -> list[dict]:
        """Retrieves list of movies/shows with the given title
        and release date.

        Args:
            title (str): movie/show title to search for
            year (int): movie's/show's release year
            _type (str): media type - TV Show or Movie

        Returns:
            list[dict]: Movies with given title and release year.
        """
        url = (
            f'{cls.base_url}?s={title}&y={year}'
            f'&type={_type}&apikey={cls.api_key}'
        )

        json_values = fetch_data(url)

        videos = []
        if json_values['Response'] == 'True':
            videos = json_values['Search']
        return videos

    @classmethod
    def search_by_title(cls, title: str, media_type: str) -> list[dict]:
        """Retrieves list of movies/shows with the given title

        Args:
            title: movie/show title to search for
            media_type: media type - TV Show or Movie

        Returns:
            list[dict]: Movies/Shows with given title.
        """
        url = (
            f'{cls.base_url}?s={title}&type={media_type}&apikey={cls.api_key}'
        )

        json_values = fetch_data(url)

        videos = []
        if json_values['Response'] == 'True':
            videos = json_values['Search']
        return videos

    @classmethod
    def lookup_by_id(cls, imdb_id: str) -> dict | None:
        """Retrieves the movie/show with the given imdb_id

        Args:
            imdb_id (str): IMDB to lookup

        Returns:
            dict: The movie data.
        """
        url = f'{cls.base_url}?i={imdb_id}&apikey={cls.api_key}'

        json_values = fetch_data(url)

        video = None
        if json_values['Response'] == 'True':
            video = {
                'title': json_values['Title'],
                'year': json_values['Year'],
            }
        return video
