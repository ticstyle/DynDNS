# number.py
"""Number platform for DynDNS integration."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.components.number import (
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.const import EntityCategory, UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DynDNSConfigEntry, DynDNSUpdateCoordinator
from .const import (
    CONF_HOSTNAME,
    CONF_PROTOCOL,
    CONF_UPDATE_INTERVAL,
    DEFAULT_UPDATE_INTERVAL_MINUTES,
    DOMAIN,
    PROTOCOL_DYNDNS2,
)

NUMBER_DESCRIPTION = NumberEntityDescription(
    key="update_interval",
    translation_key="update_interval",
    native_min_value=1,
    native_max_value=1440,
    native_step=1,
    native_unit_of_measurement=UnitOfTime.MINUTES,
    mode=NumberMode.BOX,
    entity_category=EntityCategory.CONFIG,
    icon="mdi:timer-cog-outline",
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: DynDNSConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up DynDNS number entity based on a config entry."""
    coordinator = entry.runtime_data
    async_add_entities([DynDNSUpdateIntervalNumber(coordinator, entry)])


class DynDNSUpdateIntervalNumber(
    CoordinatorEntity[DynDNSUpdateCoordinator], NumberEntity
):
    """Representation of an update interval configuration number entity."""

    entity_description = NUMBER_DESCRIPTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DynDNSUpdateCoordinator,
        entry: DynDNSConfigEntry,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(coordinator)
        self._entry = entry

        hostname: str = entry.data[CONF_HOSTNAME]
        protocol: str = entry.data.get(CONF_PROTOCOL, PROTOCOL_DYNDNS2)

        formatted_domain = hostname.lower().replace(".", "_").replace("-", "_")
        formatted_proto = protocol.lower().replace("-", "_")

        self.entity_id = (
            f"number.dyndns_{formatted_proto}_update_interval_{formatted_domain}"
        )
        self._attr_unique_id = f"{entry.entry_id}_update_interval"
        self._attr_name = "Update Interval"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"DynDNS ({hostname} - {protocol.upper()})",
            manufacturer="ticstyle",
            model=f"DynDNS ({protocol.upper()})",
        )

    @property
    def native_value(self) -> int:
        """Return the current update interval as an integer."""
        return int(
            self._entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL_MINUTES)
        )

    async def async_set_native_value(self, value: float) -> None:
        """Set new update interval and reconfigure coordinator polling."""
        minutes = int(value)

        # Update coordinator polling interval dynamically
        self.coordinator.update_interval = timedelta(minutes=minutes)

        # Persist entry data to disk
        new_data = {**self._entry.data, CONF_UPDATE_INTERVAL: minutes}
        self.hass.config_entries.async_update_entry(self._entry, data=new_data)

        # Notify Home Assistant of updated state
        self.async_write_ha_state()
