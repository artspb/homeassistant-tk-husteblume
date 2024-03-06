"""Sensor platform for TK Husteblume."""

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorEntityDescription

from . import CONF_STATION
from .const import DOMAIN
from .const import ICON
from .entity import TkHusteblumeEntity

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup_entry(hass, config_entry, async_add_devices):
    """Setup sensor platform."""
    _LOGGER.info("Creating entities")
    station = config_entry.data[CONF_STATION]
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    devices = []
    for allergen in coordinator.data:
        devices.append(TkHusteblumeSensor(station, allergen, coordinator, config_entry))
    async_add_devices(devices)
    _LOGGER.info(f"Created {len(devices)} entities")


class TkHusteblumeSensor(TkHusteblumeEntity, SensorEntity):
    """tk_husteblume Sensor class."""

    def __init__(self, station, allergen, coordinator, config_entry):
        super().__init__(coordinator, config_entry)
        self.entity_description = SensorEntityDescription(
            key=allergen,
            has_entity_name=True,
            icon=ICON,
            device_class=f"{DOMAIN}__allergen_device_class",
            translation_key=allergen,
        )
        self.station = station
        self.allergen = allergen

    @property
    def native_value(self):
        """Return the state of the sensor."""
        values = self.coordinator.data.get(self.allergen)
        return values[0] if len(values) > 0 else None

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sensor."""
        values = self.coordinator.data.get(self.allergen)
        return (
            {
                "tomorrow": values[1],
                "day_after_tomorrow": values[2],
            }
            if len(values) > 2
            else None
        )
