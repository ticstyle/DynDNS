# __init__.py
"""The DynDNS integration."""

from __future__ import annotations

from datetime import timedelta
import logging

import aiohttp

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    CONF_HOSTNAME,
    CONF_PASSWORD,
    CONF_SERVER,
    CONF_USERNAME,
    DOMAIN,
    UPDATE_INTERVAL_MINUTES,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BUTTON]

type DynDNSConfigEntry = ConfigEntry[DynDNSUpdateCoordinator]


class DynDNSUpdateCoordinator(DataUpdateCoordinator[str]):
    """Class to manage fetching DynDNS IP updates."""

    config_entry: DynDNSConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        entry: DynDNSConfigEntry,
    ) -> None:
        """Initialize the update coordinator."""
        self.server: str = entry.data[CONF_SERVER]
        self.hostname: str = entry.data[CONF_HOSTNAME]
        self.username: str = entry.data[CONF_USERNAME]
        self.password: str = entry.data[CONF_PASSWORD]
        self.last_ip: str | None = None

        super().__init__(
            hass,
            _LOGGER,
            name=f"DynDNS ({self.hostname})",
            update_interval=timedelta(minutes=UPDATE_INTERVAL_MINUTES),
        )

    async def _async_update_data(self) -> str:
        """Perform DynDNS2 protocol update call."""
        session = async_get_clientsession(self.hass)
        url = f"https://{self.server}/nic/update"
        params = {"hostname": self.hostname}
        auth = aiohttp.BasicAuth(self.username, self.password)

        try:
            async with session.get(
                url,
                params=params,
                auth=auth,
                headers={"User-Agent": "HomeAssistant-DynDNS/1.0"},
                timeout=aiohttp.ClientTimeout(total=15),
            ) as response:
                text = (await response.text()).strip()

                if response.status == 401 or "badauth" in text:
                    raise UpdateFailed("Authentication failed for DynDNS update")

                # Parse standard DynDNS2 responses (good 1.2.3.4 or nochg 1.2.3.4)
                parts = text.split()
                if parts and parts[0] in ("good", "nochg") and len(parts) > 1:
                    self.last_ip = parts[1]
                    return parts[1]

                # If IP wasn't returned in string, fallback to previous known IP or response
                if self.last_ip:
                    return self.last_ip

                return text
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with DynDNS server: {err}") from err


async def async_setup_entry(hass: HomeAssistant, entry: DynDNSConfigEntry) -> bool:
    """Set up DynDNS from a config entry."""
    coordinator = DynDNSUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: DynDNSConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_entry(entry, PLATFORMS)
    
