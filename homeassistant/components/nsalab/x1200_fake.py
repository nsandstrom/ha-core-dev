"""A mocked implementation of the x1200."""

import random

from .x1200 import BaseUps


class X1200(BaseUps):
    """A mocked implementation of the x1200."""

    def __init__(
        self, i2c_bus: int, i2c_address: int, gpoi_chip: int, pld_pin: int
    ) -> None:
        """Create a mocked x1200."""
        super().__init__(i2c_bus, i2c_address, gpoi_chip, pld_pin)

        self._local_pld_state = "on"

    def _read_level(self):
        if self._i2c_address == int("0x66", 16):
            raise MockedSMbusError("Fake sensor always fails on address 0x66") from None
        return random.randint(0, 100)

    def _read_voltage(self) -> float:
        return random.random() * 1.2 + 3

    def _read_pld(self) -> bool:
        if random.randint(0, 10) > 8:
            self._local_pld_state = not self._local_pld_state
        return self._local_pld_state


class MockedSMbusError(ConnectionError):
    """Error to indicate we cannot connect."""
