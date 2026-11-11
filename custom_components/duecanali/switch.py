"""Power switch (inverse of the amp's Standby flag)."""
from __future__ import annotations

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN, PATH_STANDBY
from .entity import DuecanaliEntity


async def async_setup_entry(hass, entry, async_add_entities):
    async_add_entities([DuecanaliPowerSwitch(entry.runtime_data)])


class DuecanaliPowerSwitch(DuecanaliEntity, SwitchEntity):
    _attr_name = "Power"

    def __init__(self, coordinator) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{DOMAIN}_{coordinator.host}_power"

    @property
    def is_on(self) -> bool:
        # Standby false = amp awake = switch on
        return not self.coordinator.data["standby"]

    async def async_turn_on(self, **kwargs) -> None:
        await self.coordinator.client.write_bool(PATH_STANDBY, False)
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs) -> None:
        await self.coordinator.client.write_bool(PATH_STANDBY, True)
        await self.coordinator.async_request_refresh()
