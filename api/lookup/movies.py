from api.lookup.util import fetch_data


class VideoLookup:
    base_url = "http://www.omdbapi.com"
    api_key = "4abce0f7"  # TODO Move to config file

    @classmethod
    def search_by_title_year(cls, title: str, year: int, _type: str) -> dict:
        url = f"{cls.base_url}?s={title}&y={year}&type={_type}&apikey={cls.api_key}"

        json_values = fetch_data(url)

        if json_values["Response"] == "True":
            return json_values["Search"]

    @classmethod
    def search_by_title(cls, title: str, media_type: str) -> dict:
        url = f"{cls.base_url}?s={title}&type={media_type}&apikey={cls.api_key}"

        json_values = fetch_data(url)

        if json_values["Response"] == "True":
            return json_values["Search"]

    @classmethod
    def lookup_by_title(cls, title: str, year: int, _type: str) -> dict:
        url = f"{cls.base_url}?t={title}&y={year}&type={_type}&apikey={cls.api_key}"

        json_values = fetch_data(url)

        if json_values["Response"] == "True":
            return {'imdb_id': json_values['imdbID']}

    @classmethod
    def lookup_by_id(cls, imdb_id: str) -> dict:
        url = f"{cls.base_url}?i={imdb_id}&apikey={cls.api_key}"

        json_values = fetch_data(url)

        if json_values["Response"] == "True":
            return {'title': json_values['Title'], 'year': json_values['Year']}
