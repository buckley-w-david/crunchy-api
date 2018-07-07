import logging
import json
import random
from string import Template
import typing
from urllib.parse import urlencode
from urllib.request import urlopen

from crunchy_api.types import Field, ObjectType, MediaType, SortMode

__version__ = "0.3.0"

"""
Api documentation
https://github.com/CloudMax94/crunchyroll-api/wiki/Api
"""
API_VERSION = "0"
URL = Template(f"https://api.crunchyroll.com/$method.{API_VERSION}.json")
VERSION = "1.1.21.0"
DEVICE = "com.crunchyroll.windows.desktop"

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

def _make_request(method: str, payload: dict) -> dict:
    endpoint = URL.substitute(method=method)
    data = urlencode(payload).encode("utf-8")
    LOGGER.info("endpoint: %s\ndata: %s", endpoint, data)
    request = urlopen(endpoint, data)
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
            self = args[0]  # This feels clever in the worst kind of way
            self._session_id = _refresh_session(
                self._device_id, # pylint: disable=protected-access
                DEVICE,
                self._token, # pylint: disable=protected-access
                VERSION,
                self.locale,
                self._auth, # pylint: disable=protected-access
            )
            attempt = func(*args, **kwargs)
            if attempt["error"]:
                # Couldn't restart the session, kill everything, try authentication from the start
                self._session_id = None
                self._auth = None
        return attempt

    return retry_func


SORT = {SortMode.ASC: "asc", SortMode.DESC: "desc"}

INFO = {
    ObjectType.MEDIA: "media_id",
    ObjectType.COLLECTION: "collection_id",
    ObjectType.SERIES: "series_id",
}

MEDIA = {
    MediaType.ANIME: "anime",
    MediaType.DRAMA: "drama",
    MediaType.ANIME_DRAMA: "anime|drama",
}


class CrunchyrollApi:
    def _request(self, method, args):
        payload = args.copy()
        payload.update(version=VERSION, locale=self.locale, session_id=self._session)
        return _make_request(method, payload)

    def __init__(self, username, password, token, locale="enUS") -> None:
        self._session_id = None
        self._auth = None
        self._username = username
        self._password = password
        self._token = token
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
                self._device_id, DEVICE, self._token, VERSION, self.locale, self._auth
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
    def info(self, object_type: ObjectType, object_id: int) -> dict:
        payload = {INFO[object_type]: object_id}
        return self._request("info", payload)

    @retry_on_error
    def list_locales(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    @retry_on_error
    def list_media(
        self,
        object_type: ObjectType,
        object_id: int,
        sort: SortMode = SortMode.ASC,
        offset: int = 0,
        locale: str = None,
    ) -> dict:
        locale = locale or self.locale
        payload = {
            INFO[object_type]: object_id,
            sort: SORT[sort],
            offset: offset,
            locale: locale,
        }
        return self._request("list_media", payload)

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
        payload = {"auth": self._auth}
        result = self._request("logout", payload)
        self._auth = None
        return result

    @retry_on_error
    def queue(
        self, media_types: MediaType, fields: typing.Iterable[Field] = tuple()
    ) -> dict:
        payload = {
            "media_types": MEDIA[media_types],
            "fields": ",".join([Field.to_str(field) for field in fields]),
        }
        return self._request("queue", payload)

    @retry_on_error
    def recently_watched(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")

    @retry_on_error
    def remove_from_queue(self) -> dict:
        raise NotImplementedError("Haven't gotten to this yet")
