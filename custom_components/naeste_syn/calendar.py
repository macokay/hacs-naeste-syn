"""Calendar platform for Næste Syn."""

from __future__ import annotations

from datetime import date, datetime, timedelta
import logging

from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    FIELD_MAKE,
    FIELD_MODEL,
    FIELD_MOT_INFO,
    FIELD_NEXT_INSPECTION,
    FIELD_MOT_DATE,
)
from .coordinator import NaesteSynCoordinator

_LOGGER = logging.getLogger(__name__)

# Tuples of (mot_info sub-key, calendar event summary label)
CALENDAR_EVENTS = [
    (FIELD_NEXT_INSPECTION, "Periodic Inspection"),
    (FIELD_MOT_DATE, "MOT Deadline"),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Næste Syn calendar entity."""
    coordinator: NaesteSynCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([NaesteSynCalendar(coordinator, entry)])


class NaesteSynCalendar(CoordinatorEntity[NaesteSynCoordinator], CalendarEntity):
    """Calendar entity showing upcoming inspection dates for a vehicle."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: NaesteSynCoordinator, entry: ConfigEntry) -> None:
        """Initialise the calendar entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_calendar"
        self._attr_name = f"Inspection {coordinator.registration}"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info for this vehicle."""
        d = self.coordinator.data or {}
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.registration)},
            name=f"Vehicle {self.coordinator.registration}",
            manufacturer=d.get(FIELD_MAKE) or "Unknown",
            model=d.get(FIELD_MODEL) or None,
        )

    def _build_events(self) -> list[CalendarEvent]:
        """Build CalendarEvent objects from coordinator data."""
        data = self.coordinator.data
        if not data:
            return []

        mot = data.get(FIELD_MOT_INFO) or {}
        make  = data.get(FIELD_MAKE, "")
        model = data.get(FIELD_MODEL, "")
        description = f"{make} {model}".strip() or self.coordinator.registration

        events: list[CalendarEvent] = []
        seen: set[str] = set()

        for sub_key, label in CALENDAR_EVENTS:
            date_str = mot.get(sub_key)
            if not date_str or str(date_str) in seen:
                continue
            seen.add(str(date_str))
            try:
                d = date.fromisoformat(str(date_str)[:10])
                start = datetime(d.year, d.month, d.day, 8, 0, 0)
                events.append(
                    CalendarEvent(
                        start=start,
                        end=start + timedelta(hours=2),
                        summary=f"{label} — {self.coordinator.registration}",
                        description=description,
                    )
                )
            except (ValueError, TypeError):
                _LOGGER.warning(
                    "Næste Syn calendar: could not parse date '%s' for key '%s'",
                    date_str,
                    sub_key,
                )

        return events

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event (required by CalendarEntity)."""
        now = datetime.now()
        upcoming = [e for e in self._build_events() if e.end >= now]
        return min(upcoming, key=lambda e: e.start) if upcoming else None

    async def async_get_events(
        self,
        hass: HomeAssistant,
        start_date: datetime,
        end_date: datetime,
    ) -> list[CalendarEvent]:
        """Return all events within the requested date range."""
        return [e for e in self._build_events() if start_date <= e.start <= end_date]
