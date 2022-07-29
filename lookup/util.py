import json
import urllib.request as ur


def fetch_data(url: str) -> dict:
    """ Retrieves json data from given url """
    return json.loads(ur.urlopen(url).read())


def sanitize(data: str) -> str:
    """ Sanitizes the given string for use in url """
    return data.replace(' ', '+')
