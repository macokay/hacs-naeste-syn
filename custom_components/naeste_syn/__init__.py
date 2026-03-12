"""Næste Syn integration for Home Assistant.

Tracks vehicle inspection dates using the MotorAPI (motorapi.dk).
"""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_API_KEY, CONF_REGISTRATION
from .coordinator import NaesteSynCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor", "calendar"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Næste Syn from a config entry."""
    coordinator = NaesteSynCoordinator(
        hass,
        entry.data[CONF_API_KEY],
        entry.data[CONF_REGISTRATION],
    )

    # First refresh — raises ConfigEntryNotReady on failure so HA retries automatically.
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Reload the entry when options change so optional sensors are created/removed.
    entry.async_on_unload(entry.add_update_listener(_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok


async def _reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload the entry after options are updated."""
    await hass.config_entries.async_reload(entry.entry_id)
