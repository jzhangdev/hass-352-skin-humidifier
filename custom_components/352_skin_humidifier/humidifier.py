"""Platform for 352 skin humidifier integration."""
from __future__ import annotations

from homeassistant.components.humidifier import (
    HumidifierEntity,
    HumidifierEntityFeature,
)
from homeassistant.components.humidifier.const import HumidifierAction
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import DeviceStatusResponse, SkinHumidifierCoordinator
from .const import HumidifierConf, HumidifierMode, HumidityLimit


async def async_setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType,
):
    """Async setup entity."""
    name = config[HumidifierConf.NAME]
    device_id = config[HumidifierConf.DEVICE_ID]
    token = config[HumidifierConf.TOKEN]
    coordinator = SkinHumidifierCoordinator(hass, device_id=device_id, token=token)
    await coordinator.async_config_entry_first_refresh()
    add_entities([SkinHumidifier(coordinator, name)])


class SkinHumidifier(CoordinatorEntity, HumidifierEntity):
    """352 skin humidifier entity."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, name) -> None:
        """Initialize entity."""
        super().__init__(coordinator)
        self._attr_is_on = False
        self._attr_name = name
        self._attr_supported_features = HumidifierEntityFeature(1)
        self._attr_available_modes = [
            HumidifierMode.AUTO,
            HumidifierMode.COMFORT,
            HumidifierMode.SLEEP,
            HumidifierMode.HUMIDITY_FIRST,
            HumidifierMode.WIND_SPEED_FIRST,
        ]
        self._attr_mode = None
        self._attr_action = HumidifierAction.OFF
        self._attr_current_humidity = None
        self._attr_target_humidity = None
        self._attr_current_temperature = None

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        device: DeviceStatusResponse = self.coordinator.data
        device_property = device.data["property"]
        self._attr_is_on = bool(device_property["PowerSwitch"]["value"])
        self._attr_current_humidity = device_property["RelativeHumidity"]["value"]
        self._attr_target_humidity = device_property["SetHumidity"]["value"]
        # 1: Auto, 2: Comfort, 3: Sleep, 4: Humidity First, 5: Wind speed first
        self._attr_mode = self.available_modes[device_property["WorkMode"]["value"] - 1]
        self._attr_current_temperature = device_property["CurrentTemperature"]["value"]
        self.async_write_ha_state()

    @property
    def name(self):
        """Entity name."""
        return self._attr_name

    @property
    def min_humidity(self):
        """Return the minimum humidity."""
        return HumidityLimit.MIN

    @property
    def max_humidity(self):
        """Return the maximum humidity."""
        return HumidityLimit.MAX

    def turn_on(self):
        """Turn the entity on."""
        self._attr_is_on = True

    def turn_off(self):
        """Turn the entity off."""
        self._attr_is_on = False

    def set_mode(self, mode):
        """Set new mode."""
        self._attr_mode = mode

    def set_humidity(self, humidity: int):
        """Set new target humidity."""
        self._attr_target_humidity = humidity

    @property
    def action(self):
        """Return current status."""
        if self._attr_is_on:
            return HumidifierAction.HUMIDIFYING
        else:
            return HumidifierAction.OFF

    @property
    def extra_state_attributes(self):
        """Return entity specific state attributes."""
        return {"current_temperature": self._attr_current_temperature}
