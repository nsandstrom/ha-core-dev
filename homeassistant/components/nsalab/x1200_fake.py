"""A mocked implementation of the x1200."""

import datetime
import random

from .x1200 import BaseUpsHat


class X1200(BaseUpsHat):
    """A mocked implementation of the x1200."""

    def __init__(self, i2c_bus: int, i2c_address: int) -> None:
        """Create a mocked x1200."""
        super().__init__(i2c_bus, i2c_address)

        # self._i2c_address = i2c_address
        print("🔌 Connect fake SMBUS", i2c_bus)

    def _read_level(self):
        if self._i2c_address == int("0x66", 16):
            raise MockedSMbusError("Fake sensor always fails on address 0x66") from None
        return random.randint(0, 100)

    @property
    def battery_level(self) -> int:
        """Battery level as a percentage."""
        print("🔋 ask for battery_level", datetime.datetime.now())
        level = self._read_level()
        return round(level, 2)

    @property
    def battery_voltage(self) -> float:
        """Return a random voltage roughly that of a 12v battery."""
        print("🔋 ask for battery_voltage", datetime.datetime.now())
        return round(random.random() * 3 + 10, 2)


class MockedSMbusError(ConnectionError):
    """Error to indicate we cannot connect."""
