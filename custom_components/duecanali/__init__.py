"""Powersoft Duecanali integration."""
from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import DuecanaliClient, DuecanaliError
from .const import DOMAIN, PATH_SLOT, PATH_STANDBY, SCAN_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)
PLATFORMS = [Platform.SWITCH, Platform.SENSOR]


class DuecanaliCoordinator(DataUpdateCoordinator[dict]):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, client: DuecanaliClient) -> None:
        super().__init__(
            hass,
            _LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL_SECONDS),
        )
        self.client = client
        self.host = entry.data[CONF_HOST]

    async def _async_update_data(self) -> dict:
        try:
            standby = await self.client.read_bool(PATH_STANDBY)
        except DuecanaliError as err:
            raise UpdateFailed(str(err)) from err

        slot = None
        try:
            slot = await self.client.read_raw_value(PATH_SLOT)
        except DuecanaliError as err:
            _LOGGER.debug("Could not read preset slot: %s", err)

        return {"standby": standby, "slot": slot}


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    client = DuecanaliClient(async_get_clientsession(hass), entry.data[CONF_HOST])
    coordinator = DuecanaliCoordinator(hass, entry, client)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
