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
    CONF_UPDATE_INTERVAL,
    CONF_USERNAME,
    DEFAULT_SERVER,
    DEFAULT_UPDATE_INTERVAL_MINUTES,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class DynDNSConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for DynDNS."""

    VERSION = 1

    async def _async_validate_input(
        self, user_input: dict[str, Any]
    ) -> tuple[dict[str, str], str]:
        """Validate user credentials against DynDNS server."""
        errors: dict[str, str] = {}
        hostname = user_input[CONF_HOSTNAME].strip().lower()

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
                    if "badauth" in text:
                        errors["base"] = "invalid_auth"
                    elif "nohost" in text or "notfqdn" in text:
                        errors["base"] = "cannot_connect"
        except (aiohttp.ClientError, TimeoutError):
            errors["base"] = "cannot_connect"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected error during DynDNS configuration")
            errors["base"] = "unknown"

        return errors, hostname

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            errors, hostname = await self._async_validate_input(user_input)

            if not errors:
                await self.async_set_unique_id(hostname)
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=hostname,
                    data={
                        CONF_SERVER: user_input[CONF_SERVER].strip(),
                        CONF_HOSTNAME: hostname,
                        CONF_USERNAME: user_input[CONF_USERNAME].strip(),
                        CONF_PASSWORD: user_input[CONF_PASSWORD].strip(),
                        CONF_UPDATE_INTERVAL: user_input[CONF_UPDATE_INTERVAL],
                    },
                )

        step_user_data_schema = vol.Schema(
            {
                vol.Required(CONF_SERVER, default=DEFAULT_SERVER): str,
                vol.Required(CONF_HOSTNAME): str,
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(
                    CONF_UPDATE_INTERVAL,
                    default=DEFAULT_UPDATE_INTERVAL_MINUTES,
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=1440)),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=step_user_data_schema,
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle reconfiguration of an existing entry via the UI cogwheel."""
        reconfig_entry = self._get_reconfigure_entry()
        errors: dict[str, str] = {}

        if user_input is not None:
            errors, hostname = await self._async_validate_input(user_input)

            if not errors:
                return self.async_update_reload_and_abort(
                    reconfig_entry,
                    data={
                        CONF_SERVER: user_input[CONF_SERVER].strip(),
                        CONF_HOSTNAME: hostname,
                        CONF_USERNAME: user_input[CONF_USERNAME].strip(),
                        CONF_PASSWORD: user_input[CONF_PASSWORD].strip(),
                        CONF_UPDATE_INTERVAL: user_input[CONF_UPDATE_INTERVAL],
                    },
                )

        reconfig_schema = vol.Schema(
            {
                vol.Required(
                    CONF_SERVER,
                    default=reconfig_entry.data.get(CONF_SERVER, DEFAULT_SERVER),
                ): str,
                vol.Required(
                    CONF_HOSTNAME,
                    default=reconfig_entry.data.get(CONF_HOSTNAME, ""),
                ): str,
                vol.Required(
                    CONF_USERNAME,
                    default=reconfig_entry.data.get(CONF_USERNAME, ""),
                ): str,
                vol.Required(
                    CONF_PASSWORD,
                    default=reconfig_entry.data.get(CONF_PASSWORD, ""),
                ): str,
                vol.Required(
                    CONF_UPDATE_INTERVAL,
                    default=reconfig_entry.data.get(
                        CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL_MINUTES
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=1440)),
            }
        )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=reconfig_schema,
            errors=errors,
        )
        
