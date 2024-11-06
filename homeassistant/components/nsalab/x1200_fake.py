"""A mocked implementation of the x1200."""

import datetime
import random

from .const import POLL_TIME


class X1200:
    """A mocked implementation of the x1200."""

    def __init__(self) -> None:
        """Create a mocked x1200."""
        self.voltage = None
        self.capacity = None
        self._last_update = datetime.datetime.min

    def _update_sensors(self):
        if self._needs_update():
            self._last_update = datetime.datetime.now()
            print("👀 fake x1200 updating now")
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
        return random.randint(0, 100)

    @property
    def battery_voltage(self) -> float:
        """Return a random voltage roughly that of a 12v battery."""
        print("🔋 ask for battery_voltage", datetime.datetime.now())
        self._update_sensors()
        return round(random.random() * 3 + 10, 2)
