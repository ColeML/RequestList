from datetime import date
import json
import urllib.request as ur
import re


def fetch_data(url: str) -> dict:
    """ Retrieves json data from given url """
    return json.loads(ur.urlopen(url).read())


def sanitize(data: str) -> str:
    """ Sanitizes the given string for use in url """
    return data.replace(' ', '+')


def convert_to_date(_date: str) -> date | None:
    """ Converts the given string into a date object

    Args:
        _date: The date string to convert.

    Returns:
        date: created date object | None
    """
    if _date:
        if re.match(r'\d{2,4}(/|-)\d+(/|-)\d+', _date):
            return date.fromisoformat(_date)
        elif re.match(r'\d{2,4}(/|-)\d+', _date):
            year, month = map(int, re.split(r'\D', _date))
            return date(year, month, 1)
        elif re.match(r'\d{2,4}', _date):
            return date(int(_date), 1, 1)
