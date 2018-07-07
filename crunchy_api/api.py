import json
from string import Template
from urllib.parse import urlencode
from urllib.request import urlopen

"""
Api documentation
https://github.com/CloudMax94/crunchyroll-api/wiki/Api
"""
API_VERSION = '0'
URL = Template(f"https://api.crunchyroll.com/$method.{API_VERSION}.json")
VERSION = "1.1.21.0"
TOKEN = "LNDJgOit5yaRIWN"
DEVICE = "com.crunchyroll.windows.desktop"


def _make_request(method: str, payload: dict) -> dict:
    endpoint = URL.substitute(method=method, version=API_VERSION)
    request = urlopen(endpoint, urlencode(payload).encode('utf-8'))
    return json.loads(request.read().decode('utf-8'))


class CrunchyrollApi:

    def _request(self, method, args):
        payload = args.copy()
        payload.update(version=VERSION, locale=self.locale, session_id=self._session)
        return _make_request(method, payload)

    def _refresh_session(self, auth=None):
        self._session = 'tmp'

    def __init__(self, username, password, locale='enUS') -> None:
        self._session = None
        self._username = username
        self._password = password
        self.locale = locale
        self._refresh_session()
        self.login(username, password)

    def add_to_queue(self, series_id: int) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    def batch(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    def categories(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    def info(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    def list_locales(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    def list_media(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    def list_series(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    def log(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    def login(self, username, password) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    def logout(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    def queue(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    def recently_watched(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    def remove_from_queue(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")
