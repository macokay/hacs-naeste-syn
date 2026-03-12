"""DataUpdateCoordinator for Næste Syn."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, API_BASE_URL, API_ENDPOINT

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(hours=24)


class NaesteSynCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetches vehicle data from MotorAPI once every 24 hours."""

    def __init__(self, hass: HomeAssistant, api_key: str, registration: str) -> None:
        """Initialise the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{registration}",
            update_interval=SCAN_INTERVAL,
        )
        self._api_key = api_key
        self._registration = registration.upper().replace(" ", "")

    @property
    def registration(self) -> str:
        """Return the normalised registration number."""
        return self._registration

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch fresh vehicle data from the MotorAPI."""
        url = f"{API_BASE_URL}{API_ENDPOINT.format(registration=self._registration)}"
        headers = {"X-API-Key": self._api_key}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url, headers=headers, timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status == 401:
                        raise UpdateFailed(
                            f"Invalid API key (401 Unauthorized) for {self._registration}"
                        )
                    if resp.status == 404:
                        raise UpdateFailed(
                            f"Vehicle '{self._registration}' not found in MotorAPI (404)"
                        )
                    if resp.status >= 400:
                        raise UpdateFailed(
                            f"MotorAPI returned HTTP {resp.status} for {self._registration}"
                        )
                    return await resp.json()
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Network error contacting MotorAPI: {err}") from err
