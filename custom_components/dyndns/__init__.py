# __init__.py
"""The DynDNS integration."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

import aiohttp
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .const import (
    CONF_HOSTNAME,
    CONF_PASSWORD,
    CONF_SERVER,
    CONF_UPDATE_INTERVAL,
    CONF_USERNAME,
    DEFAULT_UPDATE_INTERVAL_MINUTES,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BUTTON, Platform.BINARY_SENSOR]

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
        update_interval_minutes: int = entry.data.get(
            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL_MINUTES
        )

        self.last_ip: str | None = None
        self.last_success_time: datetime | None = None
        self.last_update_failed: bool = False

        super().__init__(
            hass,
            _LOGGER,
            name=f"DynDNS ({self.hostname})",
            update_interval=timedelta(minutes=update_interval_minutes),
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
                    self.last_update_failed = True
                    raise UpdateFailed("Authentication failed for DynDNS update")

                parts = text.split()
                if parts and parts[0] in ("good", "nochg") and len(parts) > 1:
                    self.last_ip = parts[1]
                    self.last_success_time = dt_util.utcnow()
                    self.last_update_failed = False
                    return parts[1]

                if self.last_ip:
                    self.last_success_time = dt_util.utcnow()
                    self.last_update_failed = False
                    return self.last_ip

                self.last_success_time = dt_util.utcnow()
                self.last_update_failed = False
                return text
        except aiohttp.ClientError as err:
            self.last_update_failed = True
            raise UpdateFailed(
                f"Error communicating with DynDNS server: {err}"
            ) from err
        except Exception as err:
            self.last_update_failed = True
            raise UpdateFailed(f"Unexpected error: {err}") from err


async def async_setup_entry(hass: HomeAssistant, entry: DynDNSConfigEntry) -> bool:
    """Set up DynDNS from a config entry."""
    coordinator = DynDNSUpdateCoordinator(hass, entry)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: DynDNSConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_remove_config_entry_device(
    hass: HomeAssistant, config_entry: DynDNSConfigEntry, device_entry: dr.DeviceEntry
) -> bool:
    """Remove a device and purge config entry if device is deleted from UI."""
    return True
