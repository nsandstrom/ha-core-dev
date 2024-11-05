"""Config flow for nsalab-test integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# TODO adjust the data schema to the data that you need
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        # vol.Required(CONF_HOST): str,
        # vol.Required(CONF_USERNAME): str,
        # vol.Required(CONF_PASSWORD): str,
        vol.Optional("bus", default=12): int,
        vol.Optional("address", default="0x36"): str,
    }
)


# class PlaceholderHub:
#     """Placeholder class to make tests pass.

#     TODO Remove this placeholder class and replace with things from your PyPI package.
#     """

#     def __init__(self, host: str) -> None:
#         """Initialize."""
#         self.host = host

#     async def authenticate(self, username: str, password: str) -> bool:
#         """Test if we can authenticate with the host."""
#         return True


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """

    try:
        parsed = int(data["address"], 16)
    except ValueError:
        raise AddressIsNotHex from None

    print("⭐️", parsed)
    if parsed < 0 or parsed > 128:
        raise AddressOutOfBounds from None

    # TODO validate if address do not start with 0x

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
                print("🍎 This is where we have info", info, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
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


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class AddressIsNotHex(HomeAssistantError):
    """Error to indicate that address is not a hex number."""


class AddressOutOfBounds(HomeAssistantError):
    """Error to indicate that address is to large or small."""
