from api.lookup.util import fetch_data, sanitize, convert_to_date
from typing import Optional


class BookLookup:
    base_url = "https://www.googleapis.com/books/v1/volumes"

    @classmethod
    def search_by_title_year(cls, title: str, year: int) -> list[dict]:
        url = f"{cls.base_url}?q={sanitize(title)}"

        json_values = fetch_data(url)

        book_list = []
        if json_values:
            for book in json_values["items"]:
                release_date = book["volumeInfo"].get("publishedDate")
                if str(year) in release_date and 'en' in book["volumeInfo"]["language"]:
                    book_list.append(cls.parse_book_data(book, json=True))

        return book_list

    @classmethod
    def search_by_title(cls, title: str) -> list[dict]:
        url = f"{cls.base_url}?q={sanitize(title)}"

        json_values = fetch_data(url)

        book_list = []
        if json_values:
            for book in json_values["items"]:
                if 'en' in book["volumeInfo"]["language"]:
                    book_list.append(cls.parse_book_data(book, json=True))

        return book_list

    @classmethod
    def search_by_author(cls, author: str) -> list[dict]:
        url = f"{cls.base_url}?q=author:{sanitize(author)}"

        json_values = fetch_data(url)

        book_list = []
        if json_values:
            for book in json_values["items"]:
                if 'en' in book["volumeInfo"]["language"]:
                    book_list.append(cls.parse_book_data(book, json=True))

        return book_list

    @classmethod
    def lookup_by_isbn(cls, isbn: int) -> dict:
        url = f"{cls.base_url}?q=isbn:{isbn}"

        json_values = fetch_data(url)

        if json_values:
            return cls.parse_book_data(json_values["items"][0])

    @classmethod
    def parse_book_data(cls, book_data: dict, json: Optional[bool] = False) -> dict:
        volume_info = book_data["volumeInfo"]
        ids = volume_info.get("industryIdentifiers")
        isbn_10, isbn_13 = None, None

        for _id in ids:
            if _id["type"] == 'ISBN_13':
                isbn_13 = _id['identifier']
            elif _id["type"] == 'ISBN_10':
                isbn_10 = _id['identifier']

        release_date = volume_info.get('publishedDate')
        release_date = release_date if json else convert_to_date(release_date)

        book = {
            'title': volume_info.get('title'),
            'subtitle': volume_info.get('subtitle'),
            'authors': ', '.join(volume_info.get('authors')),
            'release_date': release_date,
            'isbn_10': isbn_10,
            'isbn_13': isbn_13
        }

        return book
