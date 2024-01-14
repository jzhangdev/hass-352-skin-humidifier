"""352 skin humidifier cloud service."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import logging

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


@dataclass
class DeviceProperty:
    """Device property object."""

    value: str | int
    time: int


@dataclass
class DeviceStatusData:
    """Device status data object."""

    porperty: dict[str, DeviceProperty]


@dataclass
class DeviceStatusResponse:
    """Device status response object."""

    code: int
    message: str
    data: dict[str, DeviceStatusData]


async def _fetchDeviceStatus(deviceId: str, token: str):
    """Fetch device status."""
    headers = {"authorization": "Token " + token}
    async with aiohttp.ClientSession(headers=headers) as session, session.get(
        "https://app.352air.com/api/device/info/" + deviceId
    ) as response:
        jsonResponse = await response.json()
        return DeviceStatusResponse(**jsonResponse)


class SkinHumidifierCoordinator(DataUpdateCoordinator):
    """352 skin humidifider coordinator."""

    def __init__(self, hass: HomeAssistant, device_id: str, token: str) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name="352 Skin Humidifier",
            update_interval=timedelta(seconds=2),
        )
        self._device_id = device_id
        self._token = token

    async def _async_update_data(self):
        return await _fetchDeviceStatus(self._device_id, self._token)
