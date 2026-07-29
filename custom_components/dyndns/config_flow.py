# config_flow.py
"""Config flow for DynDNS integration."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    CONF_HOSTNAME,
    CONF_PASSWORD,
    CONF_SERVER,
    CONF_USERNAME,
    DEFAULT_SERVER,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_SERVER, default=DEFAULT_SERVER): str,
        vol.Required(CONF_HOSTNAME): str,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


class DynDNSConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for DynDNS."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            hostname = user_input[CONF_HOSTNAME].strip().lower()

            # Ensure unique domain per config entry
            await self.async_set_unique_id(hostname)
            self._abort_if_unique_id_configured()

            # Validate connection to the DynDNS endpoint
            session = async_get_clientsession(self.hass)
            server = user_input[CONF_SERVER].strip()
            username = user_input[CONF_USERNAME].strip()
            password = user_input[CONF_PASSWORD].strip()

            url = f"https://{server}/nic/update"
            params = {"hostname": hostname}
            auth = aiohttp.BasicAuth(username, password)

            try:
                async with session.get(
                    url,
                    params=params,
                    auth=auth,
                    headers={"User-Agent": "HomeAssistant-DynDNS/1.0"},
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as response:
                    if response.status == 401:
                        errors["base"] = "invalid_auth"
                    elif response.status != 200:
                        errors["base"] = "cannot_connect"
                    else:
                        text = await response.text()
                        # Check DynDNS2 response codes
                        if "badauth" in text:
                            errors["base"] = "invalid_auth"
                        elif "nohost" in text or "notfqdn" in text:
                            errors["base"] = "cannot_connect"
            except (aiohttp.ClientError, TimeoutError):
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected error during DynDNS configuration")
                errors["base"] = "unknown"

            if not errors:
                return self.async_create_entry(
                    title=hostname,
                    data={
                        CONF_SERVER: server,
                        CONF_HOSTNAME: hostname,
                        CONF_USERNAME: username,
                        CONF_PASSWORD: password,
                    },
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
