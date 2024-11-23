"""Platform for binary sensor integration."""

from homeassistant.components.binary_sensor import BinarySensorDeviceClass
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import HubConfigEntry
from .sensor import SensorBase


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: HubConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Add sensors for passed config_entry in HA."""
    hub = config_entry.runtime_data

    new_devices = []
    new_devices.append(PldSensor(hub))

    if new_devices:
        async_add_entities(new_devices)


class PldSensor(SensorBase):
    """Representation of a Sensor."""

    device_class = BinarySensorDeviceClass.PLUG

    def __init__(self, hub) -> None:
        """Initialize the sensor."""
        super().__init__(hub)

        self._attr_unique_id = f"{self._hub.hub_id}_external_power"
        self._attr_name = f"{self._hub.name} External Power"

    @property
    def state(self) -> bool:
        """Return the state of the sensor."""
        return "on" if self._hub.external_power_connected else "off"
