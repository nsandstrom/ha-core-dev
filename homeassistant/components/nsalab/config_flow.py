"""Config flow for nsalab-test integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .hub import Hub

_LOGGER = logging.getLogger(__name__)

# TODO adjust the data schema to the data that you need
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional("bus", default=1): int,
        vol.Optional("address", default="0x36"): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    if not data["address"].startswith("0x"):
        raise AddressIsNotHex from None

    try:
        parsed = int(data["address"], 16)
    except ValueError:
        raise AddressIsNotHex from None

    if parsed < 0 or parsed > 128:
        raise AddressOutOfBounds from None

    integer_address = int(data["address"], 16)
    try:
        make_test_connection(data["bus"], integer_address)
    except Exception as error:
        raise I2cCannotConnect from error

    # Return info that you want to store in the config entry.
    print("🍌 First in conf chain", data)
    return {"title": "Name of the device"}


class ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for nsalab-test."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""

        # Check if already configured
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()

        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except I2cCannotConnect:
                _LOGGER.exception("🧨 X1200 could not connect")

                errors["base"] = "I2C Connection failed"
            except AddressIsNotHex:
                errors["base"] = "address_not_hex"
            except AddressOutOfBounds:
                errors["base"] = "Address should be between 0x00 and 0x80"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


def make_test_connection(bus: int, address: int):
    """Test connectivity using values from config flow."""
    connect_status = Hub.test_connection(bus, address)
    print("🍌 Connect status", connect_status)
    if not connect_status:
        raise UnexpectedConnectivityResult() from None


class AddressIsNotHex(HomeAssistantError):
    """Error to indicate that address is not a hex number."""


class AddressOutOfBounds(HomeAssistantError):
    """Error to indicate that address is to large or small."""


class UnexpectedConnectivityResult(Exception):
    """Connectivity test returned something we did not exect."""


class I2cCannotConnect(ConnectionError):
    """Error to indicate we cannot connect."""
