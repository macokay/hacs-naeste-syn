"""Sensor platform for Næste Syn."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
import logging
from typing import Any, Callable

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    CONF_SHOW_VIN,
    CONF_SHOW_USE,
    CONF_SHOW_MOT_MILEAGE,
    CONF_SHOW_MAKE,
    CONF_SHOW_MODEL,
    CONF_SHOW_MODEL_YEAR,
    FIELD_REGISTRATION,
    FIELD_VIN,
    FIELD_MAKE,
    FIELD_MODEL,
    FIELD_MODEL_YEAR,
    FIELD_USE,
    FIELD_MOT_INFO,
    FIELD_MOT_DATE,
    FIELD_MOT_MILEAGE,
    FIELD_NEXT_INSPECTION,
)
from .coordinator import NaesteSynCoordinator

_LOGGER = logging.getLogger(__name__)


def _mot(data: dict[str, Any]) -> dict[str, Any]:
    """Return the mot_info sub-object, or an empty dict if absent."""
    return data.get(FIELD_MOT_INFO) or {}


def _days_until(date_str: str | None) -> int | None:
    """Return the number of days from today until date_str. Negative means overdue."""
    if not date_str:
        return None
    try:
        return (date.fromisoformat(str(date_str)[:10]) - date.today()).days
    except (ValueError, TypeError):
        _LOGGER.warning("Næste Syn: could not parse date '%s'", date_str)
        return None


@dataclass
class NaesteSynSensorDescription(SensorEntityDescription):
    """Extends SensorEntityDescription with Næste Syn specifics."""

    value_fn: Callable[[dict[str, Any]], Any] = field(default=lambda _: None)
    # If set, the sensor is only created when this config key is True.
    config_key: str | None = field(default=None)


SENSORS: tuple[NaesteSynSensorDescription, ...] = (
    # -- Always-present sensors (ordered as displayed in the device page) -----
    NaesteSynSensorDescription(
        key="next_inspection_days",
        name="Days Until Next Inspection",
        icon="mdi:calendar-clock",
        native_unit_of_measurement="days",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: _days_until(_mot(d).get(FIELD_NEXT_INSPECTION)),
    ),
    NaesteSynSensorDescription(
        key="next_inspection_date",
        name="Next Inspection Date",
        icon="mdi:calendar-check",
        value_fn=lambda d: _mot(d).get(FIELD_NEXT_INSPECTION),
    ),
    NaesteSynSensorDescription(
        key="mot_date",
        name="Last Inspection Date",
        icon="mdi:calendar-check-outline",
        value_fn=lambda d: _mot(d).get(FIELD_MOT_DATE),
    ),
    # -- Optional sensors (controlled by config checkboxes) -------------------
    NaesteSynSensorDescription(
        key="mot_mileage",
        name="Mileage at Last Inspection",
        icon="mdi:counter",
        native_unit_of_measurement="km",
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: _mot(d).get(FIELD_MOT_MILEAGE),
        config_key=CONF_SHOW_MOT_MILEAGE,
    ),
    NaesteSynSensorDescription(
        key="vin",
        name="VIN",
        icon="mdi:identifier",
        value_fn=lambda d: d.get(FIELD_VIN),
        config_key=CONF_SHOW_VIN,
    ),
    NaesteSynSensorDescription(
        key="registration_number",
        name="Registration Number",
        icon="mdi:car-key",
        value_fn=lambda d: d.get(FIELD_REGISTRATION),
    ),
    NaesteSynSensorDescription(
        key="make",
        name="Make",
        icon="mdi:car",
        value_fn=lambda d: d.get(FIELD_MAKE),
        config_key=CONF_SHOW_MAKE,
    ),
    NaesteSynSensorDescription(
        key="model",
        name="Model",
        icon="mdi:car-side",
        value_fn=lambda d: d.get(FIELD_MODEL),
        config_key=CONF_SHOW_MODEL,
    ),
    NaesteSynSensorDescription(
        key="model_year",
        name="Model Year",
        icon="mdi:calendar-range",
        value_fn=lambda d: d.get(FIELD_MODEL_YEAR),
        config_key=CONF_SHOW_MODEL_YEAR,
    ),
    NaesteSynSensorDescription(
        key="use",
        name="Vehicle Use",
        icon="mdi:car-info",
        value_fn=lambda d: d.get(FIELD_USE),
        config_key=CONF_SHOW_USE,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Næste Syn sensors from a config entry."""
    coordinator: NaesteSynCoordinator = hass.data[DOMAIN][entry.entry_id]
    config = {**entry.data, **entry.options}

    async_add_entities(
        NaesteSynSensor(coordinator, entry, desc)
        for desc in SENSORS
        if desc.config_key is None or config.get(desc.config_key, True)
    )


class NaesteSynSensor(CoordinatorEntity[NaesteSynCoordinator], SensorEntity):
    """A single Næste Syn sensor entity."""

    _attr_has_entity_name = True
    entity_description: NaesteSynSensorDescription

    def __init__(
        self,
        coordinator: NaesteSynCoordinator,
        entry: ConfigEntry,
        description: NaesteSynSensorDescription,
    ) -> None:
        """Initialise the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info grouping all sensors for this vehicle."""
        d = self.coordinator.data or {}
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.registration)},
            name=f"Vehicle {self.coordinator.registration}",
            manufacturer=d.get(FIELD_MAKE) or "Unknown",
            model=d.get(FIELD_MODEL) or None,
        )

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""
        if self.coordinator.data is None:
            return None
        return self.entity_description.value_fn(self.coordinator.data)
