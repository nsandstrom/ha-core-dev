"""Generic UPS hat module."""


class BaseUpsHat:
    """Base for UPS hats."""

    def __init__(self, i2c_bus: int, i2c_address: str) -> None:
        """Initialize the sensor."""
        self._i2c_address = i2c_address

    def _read_level(self) -> int:
        pass

    @classmethod
    def test_connection(cls, i2c_bus: int, i2c_address: str) -> bool:
        """Test if we can connect on the i2c bus."""
        print("Fake x1200 testing connectivity")
        x12 = cls(i2c_bus, i2c_address)
        level = x12.battery_level
        if level >= 0 and level < 200:
            return True
        raise UnexpectedConnectivityResult(f"Battery level {level} was not expected")



class UnexpectedConnectivityResult(Exception):
    """Connectivity test returned something we did not exect."""
