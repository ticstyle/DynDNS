# binary_sensor.py
"""Binary sensor platform for DynDNS integration."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DynDNSConfigEntry, DynDNSUpdateCoordinator
from .const import CONF_HOSTNAME, CONF_PROTOCOL, DOMAIN, PROTOCOL_DYNDNS2

STATUS_BINARY_SENSOR_DESCRIPTION = BinarySensorEntityDescription(
    key="update_status",
    translation_key="update_status",
    device_class=BinarySensorDeviceClass.PROBLEM,
    entity_category=EntityCategory.DIAGNOSTIC,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: DynDNSConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up DynDNS binary sensor based on a config entry."""
    coordinator = entry.runtime_data
    async_add_entities([DynDNSStatusBinarySensor(coordinator, entry)])


class DynDNSStatusBinarySensor(
    CoordinatorEntity[DynDNSUpdateCoordinator], BinarySensorEntity
):
    """Representation of a DynDNS update status binary sensor."""

    entity_description = STATUS_BINARY_SENSOR_DESCRIPTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DynDNSUpdateCoordinator,
        entry: DynDNSConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)

        hostname: str = entry.data[CONF_HOSTNAME]
        protocol: str = entry.data.get(CONF_PROTOCOL, PROTOCOL_DYNDNS2)

        formatted_domain = hostname.lower().replace(".", "_").replace("-", "_")
        formatted_proto = protocol.lower().replace("-", "_")

        self.entity_id = (
            f"binary_sensor.dyndns_{formatted_proto}_status_{formatted_domain}"
        )
        self._attr_unique_id = f"{entry.entry_id}_update_status"
        self._attr_name = "Update Failure Status"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"DynDNS ({hostname} - {protocol.upper()})",
            manufacturer="ticstyle",
            model=f"DynDNS ({protocol.upper()})",
        )

    @property
    def is_on(self) -> bool:
        """Return true if the last update failed (Problem detected)."""
        return self.coordinator.last_update_failed
