"""352 skin humidifier consts."""
from enum import IntEnum, StrEnum


class HumidifierConf(StrEnum):
    """352 skin humidifier entity config."""

    NAME = "name"
    DEVICE_ID = "device_id"
    TOKEN = "token"


class HumidifierMode(StrEnum):
    """352 skin humidifier mode."""

    AUTO = "auto"
    COMFORT = "comfort"
    SLEEP = "sleep"
    HUMIDITY_FIRST = "Humidity First"
    WIND_SPEED_FIRST = "Wind Speed First"


class HumidityLimit(IntEnum):
    """Humidity limit of the 352 skin humidifier."""

    MIN = 30
    MAX = 85
