import json
import re
import urllib.request as ur
from datetime import date


def fetch_data(url: str) -> dict:
    """Retrieves json data from given url

    Args:
        url (str): url to open

    Returns:
        dict: json data from url
    """
    return json.loads(ur.urlopen(url).read())


def sanitize(data: str) -> str:
    """Sanitizes the given string for use in url

    Args:
        data (str): Data to sanitize.

    Returns:
        str: the sanitized data
    """
    return data.replace(' ', '+')


def convert_to_date(_date: str) -> date | None:
    """Converts the given string into a date object

    Args:
        _date (str): The date string to convert.

    Returns:
        date | None: created date object or None if invalid string
    """
    converted_date = None
    if _date:
        if re.match(r'\d{2,4}(/|-)\d+(/|-)\d+', _date):
            converted_date = date.fromisoformat(_date)
        elif re.match(r'\d{2,4}(/|-)\d+', _date):
            year, month = map(int, re.split(r'\D', _date))
            converted_date = date(year, month, 1)
        elif re.match(r'\d{2,4}', _date):
            converted_date = date(int(_date), 1, 1)
    return converted_date
