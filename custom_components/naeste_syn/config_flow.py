"""Config flow for Næste Syn."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    DOMAIN,
    API_BASE_URL,
    API_ENDPOINT,
    API_AUTH_HEADER,
    CONF_API_KEY,
    CONF_REGISTRATION,
    CONF_SHOW_VIN,
    CONF_SHOW_USE,
    CONF_SHOW_MOT_MILEAGE,
    CONF_SHOW_MAKE,
    CONF_SHOW_MODEL,
    CONF_SHOW_MODEL_YEAR,
)

_LOGGER = logging.getLogger(__name__)


class _CannotConnect(Exception):
    pass


class _InvalidAuth(Exception):
    pass


class _VehicleNotFound(Exception):
    pass


async def _validate(api_key: str, registration: str) -> None:
    """Verify API key and registration number against MotorAPI."""
    reg = registration.upper().replace(" ", "")
    url = f"{API_BASE_URL}{API_ENDPOINT.format(registration=reg)}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url,
                headers={API_AUTH_HEADER: api_key},
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                if resp.status == 401:
                    raise _InvalidAuth
                if resp.status == 404:
                    raise _VehicleNotFound
                if resp.status >= 400:
                    raise _CannotConnect
    except aiohttp.ClientError as err:
        raise _CannotConnect from err


class NaesteSynConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the initial setup flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the user setup step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                await _validate(user_input[CONF_API_KEY], user_input[CONF_REGISTRATION])
            except _InvalidAuth:
                errors["base"] = "invalid_auth"
            except _VehicleNotFound:
                errors["base"] = "vehicle_not_found"
            except _CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:
                _LOGGER.exception("Unexpected error during Næste Syn setup")
                errors["base"] = "unknown"
            else:
                reg = user_input[CONF_REGISTRATION].upper().replace(" ", "")
                await self.async_set_unique_id(reg)
                self._abort_if_unique_id_configured()
                user_input[CONF_REGISTRATION] = reg
                return self.async_create_entry(title=f"Vehicle {reg}", data=user_input)

        schema = vol.Schema(
            {
                vol.Required(CONF_API_KEY): str,
                vol.Required(CONF_REGISTRATION): str,
                vol.Optional(CONF_SHOW_VIN, default=True): bool,
                vol.Optional(CONF_SHOW_USE, default=False): bool,
                vol.Optional(CONF_SHOW_MOT_MILEAGE, default=True): bool,
                vol.Optional(CONF_SHOW_MAKE, default=True): bool,
                vol.Optional(CONF_SHOW_MODEL, default=True): bool,
                vol.Optional(CONF_SHOW_MODEL_YEAR, default=True): bool,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(
        entry: config_entries.ConfigEntry,
    ) -> NaesteSynOptionsFlow:
        """Return the options flow handler."""
        return NaesteSynOptionsFlow(entry)


class NaesteSynOptionsFlow(config_entries.OptionsFlow):
    """Handle options updates (toggle optional sensors)."""

    def __init__(self, entry: config_entries.ConfigEntry) -> None:
        """Initialise the options flow."""
        self._entry = entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the options step."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current = {**self._entry.data, **self._entry.options}
        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_SHOW_VIN, default=current.get(CONF_SHOW_VIN, True)
                ): bool,
                vol.Optional(
                    CONF_SHOW_USE, default=current.get(CONF_SHOW_USE, False)
                ): bool,
                vol.Optional(
                    CONF_SHOW_MOT_MILEAGE,
                    default=current.get(CONF_SHOW_MOT_MILEAGE, True),
                ): bool,
                vol.Optional(
                    CONF_SHOW_MAKE, default=current.get(CONF_SHOW_MAKE, True)
                ): bool,
                vol.Optional(
                    CONF_SHOW_MODEL, default=current.get(CONF_SHOW_MODEL, True)
                ): bool,
                vol.Optional(
                    CONF_SHOW_MODEL_YEAR,
                    default=current.get(CONF_SHOW_MODEL_YEAR, True),
                ): bool,
            }
        )
        return self.async_show_form(step_id="init", data_schema=schema)
