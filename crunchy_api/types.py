import enum

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
    def from_str(field: str) -> 'Field':
        return getattr(Field, field.replace('.', '_').upper())

    #TODO: Replace this with a map
    @staticmethod
    def to_str(field: "Field") -> str:
        return str(field).replace("_", ".").lower()

class MediaType(enum.Enum):
    ANIME = enum.auto()
    DRAMA = enum.auto()
    ANIME_DRAMA = enum.auto()

    @staticmethod
    def from_str(media: str) -> 'MediaType':
        return getattr(MediaType, media.replace('|', '_').upper())


class ObjectType(enum.Enum):
    MEDIA = enum.auto()
    COLLECTION = enum.auto()
    SERIES = enum.auto()

    @staticmethod
    def from_str(obj: str) -> 'MediaType':
        return getattr(ObjectType, obj.upper()[:-3])


class SortMode(enum.Enum):
    ASC = enum.auto()
    DESC = enum.auto()

    @staticmethod
    def from_str(sort: str) -> 'MediaType':
        return getattr(SortMode, sort.upper())
