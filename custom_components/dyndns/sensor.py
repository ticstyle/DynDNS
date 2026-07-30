# sensor.py
"""Sensor platform for DynDNS integration."""

from __future__ import annotations

from datetime import datetime

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DynDNSConfigEntry, DynDNSUpdateCoordinator
from .const import CONF_HOSTNAME, CONF_PROTOCOL, CONF_USERNAME, DOMAIN, PROTOCOL_DYNDNS2

MAIN_SENSOR_DESCRIPTION = SensorEntityDescription(
    key="dyndns_status",
    translation_key="dyndns_status",
    icon="mdi:dns",
)

TIMESTAMP_SENSOR_DESCRIPTION = SensorEntityDescription(
    key="last_successful_update",
    translation_key="last_successful_update",
    device_class=SensorDeviceClass.TIMESTAMP,
    entity_category=EntityCategory.DIAGNOSTIC,
    icon="mdi:clock-check-outline",
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: DynDNSConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up DynDNS sensors based on a config entry."""
    coordinator = entry.runtime_data
    async_add_entities(
        [
            DynDNSSensor(coordinator, entry),
            DynDNSLastSuccessSensor(coordinator, entry),
        ]
    )


class DynDNSSensor(
    CoordinatorEntity[DynDNSUpdateCoordinator], SensorEntity, RestoreEntity
):
    """Representation of a DynDNS status sensor with state restoration."""

    entity_description = MAIN_SENSOR_DESCRIPTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DynDNSUpdateCoordinator,
        entry: DynDNSConfigEntry,
    ) -> None:
        """Initialize the main sensor."""
        super().__init__(coordinator)

        hostname: str = entry.data[CONF_HOSTNAME]
        username: str = entry.data[CONF_USERNAME]
        protocol: str = entry.data.get(CONF_PROTOCOL, PROTOCOL_DYNDNS2)

        formatted_domain = hostname.lower().replace(".", "_").replace("-", "_")
        formatted_proto = protocol.lower().replace("-", "_")

        self.entity_id = f"sensor.dyndns_{formatted_proto}_{formatted_domain}"
        self._attr_unique_id = f"{entry.entry_id}_status"
        self._attr_name = username
        self._restored_state: str | None = None

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"DynDNS ({hostname} - {protocol.upper()})",
            manufacturer="ticstyle",
            model=f"DynDNS ({protocol.upper()})",
        )

    async def async_added_to_hass(self) -> None:
        """Handle entity restored state when added to Home Assistant."""
        await super().async_added_to_hass()

        last_state = await self.async_get_last_state()
        if last_state is not None and last_state.state not in (
            None,
            "unknown",
            "unavailable",
        ):
            self._restored_state = last_state.state
            if self.coordinator.data is None:
                self.coordinator.last_ip = last_state.state

    @property
    def native_value(self) -> str | None:
        """Return the current IP address or fall back to restored state."""
        if self.coordinator.data is not None:
            return self.coordinator.data
        return self._restored_state


class DynDNSLastSuccessSensor(
    CoordinatorEntity[DynDNSUpdateCoordinator], SensorEntity
):
    """Representation of the last successful update timestamp sensor."""

    entity_description = TIMESTAMP_SENSOR_DESCRIPTION
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: DynDNSUpdateCoordinator,
        entry: DynDNSConfigEntry,
    ) -> None:
        """Initialize the diagnostic timestamp sensor."""
        super().__init__(coordinator)

        hostname: str = entry.data[CONF_HOSTNAME]
        protocol: str = entry.data.get(CONF_PROTOCOL, PROTOCOL_DYNDNS2)

        formatted_domain = hostname.lower().replace(".", "_").replace("-", "_")
        formatted_proto = protocol.lower().replace("-", "_")

        self.entity_id = (
            f"sensor.dyndns_{formatted_proto}_last_success_{formatted_domain}"
        )
        self._attr_unique_id = f"{entry.entry_id}_last_successful_update"
        self._attr_name = "Last Successful Update"

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=f"DynDNS ({hostname} - {protocol.upper()})",
            manufacturer="ticstyle",
            model=f"DynDNS ({protocol.upper()})",
        )

    @property
    def native_value(self) -> datetime | None:
        """Return UTC datetime of the last successful update."""
        return self.coordinator.last_success_time
