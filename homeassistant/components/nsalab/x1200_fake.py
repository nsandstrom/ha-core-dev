"""A mocked implementation of the x1200."""

import datetime
import random

from .const import POLL_TIME


class X1200:
    """A mocked implementation of the x1200."""

    def __init__(self, i2c_bus: int, i2c_address: str) -> None:
        """Create a mocked x1200."""
        self.voltage = None
        self.capacity = None
        self._i2c_address = i2c_address
        self._last_update = datetime.datetime.min
        print("🔌 Connect fake SMBUS", i2c_bus)

    def _update_sensors(self):
        if self._i2c_address == "0x66":
            raise RandomSMbusError from None

        if self._needs_update():
            self._last_update = datetime.datetime.now()
            print("👀 fake x1200 updating now on address", self._i2c_address)
            self.voltage = round(random.random() * 3 + 10, 2)
            self.capacity = random.randint(0, 100)
        return True

    def _needs_update(self):
        now = datetime.datetime.now()
        if (now - self._last_update).total_seconds() > (POLL_TIME - 10):
            return True
        return False

    @property
    def battery_level(self) -> int:
        """Battery level as a percentage."""
        print("🔋 ask for battery_level", datetime.datetime.now())
        self._update_sensors()
        return round(self.capacity, 2)

    @property
    def battery_voltage(self) -> float:
        """Return a random voltage roughly that of a 12v battery."""
        print("🔋 ask for battery_voltage", datetime.datetime.now())
        self._update_sensors()
        return round(self.voltage, 2)


def test_connectivity(i2c_bus: int, i2c_address: str) -> bool:
    """Test if we can connect on the i2c bus."""
    print("Fake x1200 testing connectivity")
    # try:
    x12 = X1200(i2c_bus, i2c_address)
    level = x12.battery_level
    if level >= 0 and level < 200:
        return True
    raise UnexpectedConnectivityResult(f"Level {level} was not expected")


class RandomSMbusError(ConnectionError):
    """Error to indicate we cannot connect."""


class UnexpectedConnectivityResult(Exception):
    """Connectivity test returned something we did not exect."""
