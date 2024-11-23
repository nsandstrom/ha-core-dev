"""A simple abstraction hub."""

from __future__ import annotations

from datetime import timedelta

from homeassistant.core import HomeAssistant

from .const import DOMAIN, POLL_TIME
from .x1200_fake import X1200

SCAN_INTERVAL = timedelta(seconds=POLL_TIME)


class Hub:
    """Abstraction hub."""

    manufacturer = "Geekworm"

    def __init__(
        self,
        hass: HomeAssistant,
        i2c_bus: int,
        i2c_address: int,
        gpoi_chip: int,
        pld_pin: int,
    ) -> None:
        """Init hub."""
        self._hass = hass
        self.name = "X1200 UPS"
        self._id = DOMAIN

        self.model = "X1200 UPS Shield"

        self.x1200 = X1200(i2c_bus, i2c_address, gpoi_chip, pld_pin)

        self.online = True

    @property
    def hub_id(self) -> str:
        """ID for hub."""
        return self._id

    @staticmethod
    def test_connection(i2c_bus: int, i2c_address: int) -> bool:
        """Test connectivity to the UPS module."""
        return X1200.test_connection(i2c_bus, i2c_address)

    @property
    def battery_level(self) -> int:
        """Battery level as a percentage."""
        return self.x1200.battery_level

    @property
    def battery_voltage(self) -> float:
        """Battery voltage."""
        return self.x1200.battery_voltage

    @property
    def external_power_connected(self) -> bool:
        """If external power is pluged in."""
        return self.x1200.external_power_detected
