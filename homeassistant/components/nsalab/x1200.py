"""Generic UPS hat module."""

import struct

import gpiod
from gpiod.line import Direction, Value
from smbus import SMBus


class BaseUps:
    """Base for UPS class."""

    def __init__(
        self, i2c_bus: int, i2c_address: int, gpoi_chip: int, pld_pin: int
    ) -> None:
        """Initialize the sensor."""
        self._i2c_address = i2c_address
        self._gpio_path = f"/dev/gpiochip{gpoi_chip}"
        self._pld_pin = pld_pin

    def _read_level(self) -> float:
        pass

    def _read_voltage(self) -> float:
        pass

    def _read_pld(self) -> bool:
        pass

    @classmethod
    def test_connection(cls, i2c_bus: int, i2c_address: int) -> bool:
        """Test if we can connect on the i2c bus."""
        x12 = cls(i2c_bus, i2c_address, 0, 0)
        level = x12.battery_level
        if level >= 0 and level < 200:
            return True
        raise UnexpectedConnectivityResult(f"Battery level {level} was not expected")

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

    @property
    def external_power_detected(self) -> bool:
        """External power is connected."""
        return self._read_pld()


class X1200(BaseUps):
    """X1200 UPS hat."""

    def __init__(
        self, i2c_bus: int, i2c_address: int, gpoi_chip: int, pld_pin: int
    ) -> None:
        """Initialize the sensors."""
        super().__init__(i2c_bus, i2c_address, gpoi_chip, pld_pin)
        self._i2c = SMBus(i2c_bus)

    def _read_level(self):
        read = self._i2c.read_word_data(self._i2c_address, 4)

        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        return swapped / 256

    def _read_voltage(self):
        read = self._i2c.read_word_data(self._i2c_address, 2)

        swapped = struct.unpack("<H", struct.pack(">H", read))[0]
        return swapped * 1.25 / 1000 / 16

    def _read_pld(self):
        PLD_PIN = self._pld_pin

        result = None

        with gpiod.request_lines(
            self._gpio_path,
            consumer="x1200",
            config={
                PLD_PIN: gpiod.LineSettings(
                    direction=Direction.INPUT,
                )
            },
        ) as request:
            pld_state = request.get_value(PLD_PIN)

            if pld_state == Value.ACTIVE:
                result = True
            elif pld_state == Value.INACTIVE:
                result = False

        return result


class UnexpectedConnectivityResult(Exception):
    """Connectivity test returned something we did not expect."""
