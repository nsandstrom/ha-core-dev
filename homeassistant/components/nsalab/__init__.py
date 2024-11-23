"""Geekworm X1200 UPS integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .hub import Hub

PLATFORMS: list[Platform] = [Platform.BINARY_SENSOR, Platform.SENSOR]

type HubConfigEntry = ConfigEntry[Hub]


async def async_setup_entry(hass: HomeAssistant, entry: HubConfigEntry) -> bool:
    """Set up integration from a config entry."""

    integer_address = int(entry.data["i2c_address"], 16)

    entry.runtime_data = Hub(
        hass,
        entry.data["i2c_bus"],
        integer_address,
        entry.data["gpoi_chip"],
        entry.data["pld_pin"],
    )

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: HubConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
