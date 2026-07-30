# button.py
"""Button platform for DynDNS integration."""

from __future__ import annotations

from homeassistant.components.button import (
    ButtonEntity,
    ButtonEntityDescription,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DynDNSConfigEntry, DynDNSUpdateCoordinator
from .const import CONF_HOSTNAME, CONF_PROTOCOL, DOMAIN, PROTOCOL_DYNDNS2

BUTTON_DESCRIPTION = ButtonEntityDescription(
    key="update_now",
    translation_key="update_now",
    icon="mdi:refresh",
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: DynDNSConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up DynDNS button based on a config entry."""
    coordinator = entry.runtime_data
    async_add_entities([DynDNSUpdateButton(coordinator, entry)])


class DynDNSUpdateButton(CoordinatorEntity[DynDNSUpdateCoordinator], ButtonEntity):
    """Representation of a DynDNS update button."""

    entity_description = BUTTON_DESCRIPTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DynDNSUpdateCoordinator,
        entry: DynDNSConfigEntry,
    ) -> None:
        """Initialize the button entity."""
        super().__init__(coordinator)

        hostname: str = entry.data[CONF_HOSTNAME]
        protocol: str = entry.data.get(CONF_PROTOCOL, PROTOCOL_DYNDNS2)

        formatted_domain = hostname.lower().replace(".", "_").replace("-", "_")
        formatted_proto = protocol.lower().replace("-", "_")

        self.entity_id = (
            f"button.dyndns_{formatted_proto}_update_{formatted_domain}"
        )
        self._attr_unique_id = f"{entry.entry_id}_update_now"
        self._attr_name = "Update Now"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"DynDNS ({hostname} - {protocol.upper()})",
            manufacturer="ticstyle",
            model=f"DynDNS ({protocol.upper()})",
        )

    async def async_press(self) -> None:
        """Handle button press to trigger an update."""
        await self.coordinator.async_request_refresh()
