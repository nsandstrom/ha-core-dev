"""Platform for sensor integration."""

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo, Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import HubConfigEntry
from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: HubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for passed config_entry in HA."""
    hub = config_entry.runtime_data

    new_devices = []
    new_devices.append(BatterySensor(hub))
    new_devices.append(VoltageSensor(hub))

    if new_devices:
        async_add_entities(new_devices)


class SensorBase(Entity):
    """Base representation of a Hello World Sensor."""

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        self._hub = hub

        self.model = "Test Device"

    @property
    def device_info(self) -> DeviceInfo:
        """Return information to link this entity with the correct device."""
        return {
            "identifiers": {(DOMAIN, self._hub.hub_id)},
            "name": self._hub.name,
            "model": self._hub.model,
            "manufacturer": self._hub.manufacturer,
        }

    @property
    def available(self) -> bool:
        """Return True if ups is online."""
        return self._hub.online


class BatterySensor(SensorBase):
    """Representation of a Battery Sensor."""

    device_class = SensorDeviceClass.BATTERY
    _attr_unit_of_measurement = PERCENTAGE

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)

        self._attr_unique_id = f"{self._hub.hub_id}_battery_capacity"
        self._attr_name = f"{self._hub.name} Battery Capacity"
        self._state = self._hub.battery_level

    @property
    def state(self) -> int:
        """Return the state of the sensor."""
        return self._hub.battery_level


class VoltageSensor(SensorBase):
    """Representation of a Voltage Sensor."""

    device_class = SensorDeviceClass.VOLTAGE
    _attr_unit_of_measurement = "V"
    _attr_icon = "mdi:flash"

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)

        self._attr_unique_id = f"{self._hub.hub_id}_battery_voltage"
        self._attr_name = f"{self._hub.name} Battery Voltage"
        self._state = self._hub.battery_voltage

    @property
    def state(self) -> float:
        """Return the state of the sensor."""
        return self._hub.battery_voltage
