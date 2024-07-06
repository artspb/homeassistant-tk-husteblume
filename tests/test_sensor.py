"""Test TK Husteblume switch."""

from homeassistant.config_entries import ConfigEntryState
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.tk_husteblume import TkHusteblumeDataUpdateCoordinator
from custom_components.tk_husteblume import async_setup_entry
from custom_components.tk_husteblume.const import DOMAIN
from custom_components.tk_husteblume.sensor import TkHusteblumeSensor

from .const import MOCK_CONFIG


async def test_sensor(hass, enable_custom_integrations, bypass_get_data):
    """Test switch services."""
    # Create a mock entry so we don't have to go through config flow
    config_entry = MockConfigEntry(
        domain=DOMAIN, data=MOCK_CONFIG, entry_id="test", state=ConfigEntryState.LOADED
    )
    assert await async_setup_entry(hass, config_entry)
    await hass.async_block_till_done()
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    assert type(coordinator) is TkHusteblumeDataUpdateCoordinator

    sensor = TkHusteblumeSensor(
        "test_station", "test_allergen", coordinator, config_entry
    )
    assert sensor.device_state_attributes == {
        "attribution": "Data provided by Techniker Krankenkasse",
        "id": None,
        "integration": "tk_husteblume",
    }
    assert sensor.native_value == 0
    assert sensor.extra_state_attributes == {
        "tomorrow": "1",
        "day_after_tomorrow": "2",
    }
