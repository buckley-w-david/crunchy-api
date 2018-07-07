import enum
import json
import random
from string import Template
import typing
from urllib.parse import urlencode
from urllib.request import urlopen

"""
Api documentation
https://github.com/CloudMax94/crunchyroll-api/wiki/Api
"""
API_VERSION = "0"
URL = Template(f"https://api.crunchyroll.com/$method.{API_VERSION}.json")
VERSION = "1.1.21.0"
TOKEN = "LNDJgOit5yaRIWN"
DEVICE = "com.crunchyroll.windows.desktop"


def _make_request(method: str, payload: dict) -> dict:
    endpoint = URL.substitute(method=method)
    request = urlopen(endpoint, urlencode(payload).encode("utf-8"))
    return json.loads(request.read().decode("utf-8"))


def _refresh_session(
    device_id, device_type, access_token, version, locale, auth=None
) -> str:
    payload = {
        "device_id": device_id,
        "device_type": device_type,
        "access_token": access_token,
        "version": version,
        "locale": locale,
    }
    if auth:
        payload.update(auth=auth)

    result = _make_request("start_session", payload)
    return result["data"]["session_id"]


# Attempt to refresh the session and try again if the request fails
def retry_on_error(func):
    def retry_func(*args, **kwargs):
        attempt = func(*args, **kwargs)
        if attempt["error"]:
            self = args[0] # This feels clever in the worst kind of way
            self._session_id = _refresh_session(
                self._device_id,  # pylint: disable=protected-access
                DEVICE,
                TOKEN,
                VERSION,
                self.locale,
                self._auth,  # pylint: disable=protected-access
            )
            attempt = func(*args, **kwargs)
            if attempt['error']:
                # Couldn't restart the session, kill everything, try authentication from the start
                self._session_id = None
                self._auth = None
        return attempt

    return retry_func


class Field(enum.Enum):
    IMAGE_FULL_URL = enum.auto()
    IMAGE_FWIDE_URL = enum.auto()
    IMAGE_FWIDESTAR_URL = enum.auto()
    IMAGE_HEIGHT = enum.auto()
    IMAGE_LARGE_URL = enum.auto()
    IMAGE_MEDIUM_URL = enum.auto()
    IMAGE_SMALL_URL = enum.auto()
    IMAGE_THUMB_URL = enum.auto()
    IMAGE_WIDE_URL = enum.auto()
    IMAGE_WIDESTAR_URL = enum.auto()
    IMAGE_WIDTH = enum.auto()
    MEDIA_AVAILABILITY_NOTES = enum.auto()
    MEDIA_AVAILABLE = enum.auto()
    MEDIA_AVAILABLE_TIME = enum.auto()
    MEDIA_BIF_URL = enum.auto()
    MEDIA_CLASS = enum.auto()
    MEDIA_CLIP = enum.auto()
    MEDIA_COLLECTION_ID = enum.auto()
    MEDIA_COLLECTION_NAME = enum.auto()
    MEDIA_CREATED = enum.auto()
    MEDIA_DESCRIPTION = enum.auto()
    MEDIA_DURATION = enum.auto()
    MEDIA_EPISODE_NUMBER = enum.auto()
    MEDIA_FREE_AVAILABLE = enum.auto()
    MEDIA_FREE_AVAILABLE_TIME = enum.auto()
    MEDIA_FREE_UNAVAILABLE_TIME = enum.auto()
    MEDIA_MEDIA_ID = enum.auto()
    MEDIA_MEDIA_TYPE = enum.auto()
    MEDIA_NAME = enum.auto()
    MEDIA_PLAYHEAD = enum.auto()
    MEDIA_PREMIUM_AVAILABLE = enum.auto()
    MEDIA_PREMIUM_AVAILABLE_TIME = enum.auto()
    MEDIA_PREMIUM_ONLY = enum.auto()
    MEDIA_PREMIUM_UNAVAILABLE_TIME = enum.auto()
    MEDIA_SCREENSHOT_IMAGE = enum.auto()
    MEDIA_SERIES_ID = enum.auto()
    MEDIA_SERIES_NAME = enum.auto()
    MEDIA_STREAM_DATA = enum.auto()
    MEDIA_UNAVAILABLE_TIME = enum.auto()
    MEDIA_URL = enum.auto()
    LAST_WATCHED_MEDIA = enum.auto()
    LAST_WATCHED_MEDIA_PLAYHEAD = enum.auto()
    MOST_LIKELY_MEDIA = enum.auto()
    MOST_LIKELY_MEDIA_PLAYHEAD = enum.auto()
    ORDERING = enum.auto()
    PLAYHEAD = enum.auto()
    QUEUE_ENTRY_ID = enum.auto()
    SERIES = enum.auto()
    SERIES_CLASS = enum.auto()
    SERIES_COLLECTION_COUNT = enum.auto()
    SERIES_DESCRIPTION = enum.auto()
    SERIES_GENRES = enum.auto()
    SERIES_IN_QUEUE = enum.auto()
    SERIES_LANDSCAPE_IMAGE = enum.auto()
    SERIES_MEDIA_COUNT = enum.auto()
    SERIES_MEDIA_TYPE = enum.auto()
    SERIES_NAME = enum.auto()
    SERIES_PORTRAIT_IMAGE = enum.auto()
    SERIES_PUBLISHER_NAME = enum.auto()
    SERIES_RATING = enum.auto()
    SERIES_SERIES_ID = enum.auto()
    SERIES_URL = enum.auto()
    SERIES_YEAR = enum.auto()

    @staticmethod
    def to_str(field: 'Field') -> str:
        return str(field).replace('_', '.').lower()


class CrunchyrollApi:
    def _request(self, method, args):
        payload = args.copy()
        payload.update(version=VERSION, locale=self.locale, session_id=self._session)
        return _make_request(method, payload)

    def __init__(self, username, password, locale="enUS") -> None:
        self._session_id = None
        self._auth = None
        self._username = username
        self._password = password
        char_set = "0123456789abcdefghijklmnopqrstuvwxyz0123456789"
        self._device_id = "".join(
            [
                "".join(random.sample(char_set, 8)),
                "-KODI-",
                "".join(random.sample(char_set, 4)),
                "-",
                "".join(random.sample(char_set, 4)),
                "-",
                "".join(random.sample(char_set, 12)),
            ]
        )
        self.locale = locale
        self.login(username, password)

    @property
    def _session(self):
        if not self._session_id:
            self._session_id = _refresh_session(
                self._device_id, DEVICE, TOKEN, VERSION, self.locale, self._auth
            )
        return self._session_id


    @retry_on_error
    def add_to_queue(self, series_id: int) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    @retry_on_error
    def batch(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    @retry_on_error
    def categories(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    @retry_on_error
    def info(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    @retry_on_error
    def list_locales(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    @retry_on_error
    def list_media(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    @retry_on_error
    def list_series(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    @retry_on_error
    def log(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    @retry_on_error
    def login(self, username, password) -> dict:
        payload = {"account": username, "password": password}
        result = self._request("login", payload)
        self._auth = result["data"]["auth"]
        return result

    @retry_on_error
    def logout(self) -> dict:
        payload = {
            'auth': self._auth,
        }
        result = self._request('logout', payload)
        self._auth = None
        return result

    @retry_on_error
    def queue(self, media_types, fields: typing.Iterable[Field] = tuple()) -> dict:
        payload = {
            'media_types': media_types,
            'fields': ','.join([Field.to_str(field) for field in fields]),
        }
        return self._request('queue', payload)

    @retry_on_error
    def recently_watched(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    @retry_on_error
    def remove_from_queue(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")
