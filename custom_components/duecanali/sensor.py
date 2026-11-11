"""Preset / snapshot slot sensor."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity

from .const import DOMAIN
from .entity import DuecanaliEntity


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([DuecanaliSlotSensor(entry.runtime_data)])


class DuecanaliSlotSensor(DuecanaliEntity, SensorEntity):
    _attr_name = "Preset slot"

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_{coordinator.host}_slot"

    @property
    def native_value(self):
        return self.coordinator.data.get("slot")
