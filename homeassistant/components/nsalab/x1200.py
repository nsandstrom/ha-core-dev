"""Generic UPS hat module."""

import struct

from smbus import SMBus


class BaseUpsHat:
    """Base for UPS hats."""

    def __init__(self, i2c_bus: int, i2c_address: int) -> None:
        """Initialize the sensor."""
        self._i2c_address = i2c_address

    def _read_level(self) -> int:
        pass

    @classmethod
    def test_connection(cls, i2c_bus: int, i2c_address: int) -> bool:
        """Test if we can connect on the i2c bus."""
        print("Fake x1200 testing connectivity")
        x12 = cls(i2c_bus, i2c_address)
        level = x12.battery_level
        if level >= 0 and level < 200:
            return True
        raise UnexpectedConnectivityResult(f"Battery level {level} was not expected")


class X1200(BaseUpsHat):
    """The real UPS hat."""

    def __init__(self, i2c_bus: int, i2c_address: int) -> None:
        """Initialize the sensor."""
        super().__init__(i2c_bus, i2c_address)
        self._i2c = SMBus(i2c_bus)

    def _read_level(self):
        read = self._i2c.read_word_data(self._i2c_address, 4)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        return swapped / 256

    def _read_voltage(self):
        read = self._i2c.read_word_data(self._i2c_address, 2)
        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        return swapped * 1.25 / 1000 / 16

    @property
    def battery_level(self) -> int:
        """Battery level as a percentage."""
        level = self._read_level()
        return round(level, 2)

    @property
    def battery_voltage(self) -> float:
        """Battery voltage."""
        voltage = self._read_voltage()
        return round(voltage, 2)


class UnexpectedConnectivityResult(Exception):
    """Connectivity test returned something we did not exect."""
