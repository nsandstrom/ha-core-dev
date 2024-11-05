"""A demonstration 'hub' that connects several devices."""

from __future__ import annotations

# In a real implementation, this would be in an external library that's on PyPI.
# The PyPI package needs to be included in the `requirements` section of manifest.json
# See https://developers.home-assistant.io/docs/creating_integration_manifest
# for more information.
# This dummy hub always returns 3 rollers.
import asyncio
import datetime
from datetime import timedelta
import random

from homeassistant.core import HomeAssistant

from .const import DOMAIN

SCAN_INTERVAL = timedelta(seconds=30)


class Hub:
    """Dummy hub for Hello World example."""

    manufacturer = "Demonstration Corp"

    def __init__(self, hass: HomeAssistant, host: str) -> None:
        """Init dummy hub."""
        self._host = host
        self._hass = hass
        self.name = f"{DOMAIN}_{host}"
        self._id = host.lower()

        self.firmware_version = f"0.0.{random.randint(1, 9)}"
        self.model = "UPS Shield"

        self.online = True

    @property
    def hub_id(self) -> str:
        """ID for dummy hub."""
        return self._id

    async def test_connection(self) -> bool:
        """Test connectivity to the Dummy hub is OK."""
        await asyncio.sleep(1)
        return True

    @property
    def battery_level(self) -> int:
        """Battery level as a percentage."""
        print("🔋 Randomize battery capacity IN HUB", datetime.datetime.now())
        return random.randint(0, 100)

    @property
    def battery_voltage(self) -> float:
        """Return a random voltage roughly that of a 12v battery."""
        return round(random.random() * 3 + 10, 2)

    @property
    def illuminance(self) -> int:
        """Return a sample illuminance in lux."""
        return random.randint(0, 500)
