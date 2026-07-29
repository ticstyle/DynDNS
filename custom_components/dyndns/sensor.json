# sensor.py
"""Sensor platform for DynDNS integration."""

from __future__ import annotations

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DynDNSConfigEntry, DynDNSUpdateCoordinator
from .const import CONF_HOSTNAME, CONF_USERNAME, DOMAIN

SENSOR_DESCRIPTION = SensorEntityDescription(
    key="dyndns_status",
    translation_key="dyndns_status",
    icon="mdi:dns",
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: DynDNSConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up DynDNS sensor based on a config entry."""
    coordinator = entry.runtime_data
    async_add_entities([DynDNSSensor(coordinator, entry)])


class DynDNSSensor(CoordinatorEntity[DynDNSUpdateCoordinator], SensorEntity):
    """Representation of a DynDNS status sensor."""

    entity_description = SENSOR_DESCRIPTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DynDNSUpdateCoordinator,
        entry: DynDNSConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        
        hostname: str = entry.data[CONF_HOSTNAME]
        username: str = entry.data[CONF_USERNAME]

        # Explicit entity ID format: sensor.dyndns_test_org
        formatted_domain = hostname.lower().replace(".", "_").replace("-", "_")
        self.entity_id = f"sensor.dyndns_{formatted_domain}"
        
        # Unique identifier for entity registry
        self._attr_unique_id = f"{entry.entry_id}_status"
        
        # Friendly name set to the provided login/username
        self._attr_name = username

        # Device registry entry linking this sensor to a single device
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=hostname,
            manufacturer="DynDNS Provider",
            model="DynDNS2 Protocol",
        )

    @property
    def native_value(self) -> str | None:
        """Return the current IP address returned by the DynDNS update."""
        return self.coordinator.data
