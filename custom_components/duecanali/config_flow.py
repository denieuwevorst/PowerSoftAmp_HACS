"""Config flow: ask for the amp's IP address."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_HOST
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import DuecanaliClient, DuecanaliError
from .const import DOMAIN, PATH_STANDBY


class DuecanaliConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            host = user_input[CONF_HOST].strip()
            await self.async_set_unique_id(host)
            self._abort_if_unique_id_configured()

            client = DuecanaliClient(async_get_clientsession(self.hass), host)
            try:
                await client.read_bool(PATH_STANDBY)
            except DuecanaliError:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=f"Duecanali 1604 ({host})", data={CONF_HOST: host}
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_HOST): str}),
            errors=errors,
        )
