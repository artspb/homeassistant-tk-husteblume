"""Test TK Husteblume config flow."""

from unittest.mock import patch

import pytest
from homeassistant import config_entries
from homeassistant import data_entry_flow
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.tk_husteblume import CONF_PASSWORD
from custom_components.tk_husteblume.const import DOMAIN

from .const import MOCK_CONFIG
from .const import MOCK_FORM


# This fixture bypasses the actual setup of the integration
# since we only want to test the config flow. We test the
# actual functionality of the integration in other test modules.
@pytest.fixture(autouse=True)
def bypass_setup_fixture():
    """Prevent setup."""
    with patch(
        "custom_components.tk_husteblume.async_setup",
        return_value=True,
    ), patch(
        "custom_components.tk_husteblume.async_setup_entry",
        return_value=True,
    ), patch(
        "custom_components.tk_husteblume.async_unload_entry",
        return_value=True,
    ):
        yield


# Here we simiulate a successful config flow from the backend.
# Note that we use the `bypass_get_data` fixture here because
# we want the config flow validation to succeed during the test.
async def test_successful_config_flow(
    hass, enable_custom_integrations, bypass_get_data
):
    """Test a successful config flow."""
    # Initialize a config flow
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # Check that the config flow shows the user form as the first step
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "user"

    # If a user were to enter `test_username` for username and `test_password`
    # for password, it would result in this function call
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_FORM
    )

    # Check that the config flow is complete and a new entry is created with
    # the input data
    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result["title"] == "TEST_STATION test_app_id"
    data = result["data"]
    # a random password is generated
    data[CONF_PASSWORD] = "test_password"
    assert data == MOCK_CONFIG
    assert result["result"]


# In this case, we want to simulate a failure during the config flow.
# We use the `error_on_get_stations` mock instead of `bypass_get_data`
# (note the function parameters) to raise an Exception during
# validation of the input config.
async def test_failed_config_flow_stations(
    hass, enable_custom_integrations, error_on_get_stations
):
    """Test a failed config flow due to credential validation failure."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_ABORT
    assert result["reason"] == "unable_to_fetch_stations"


# In this case, we want to simulate a failure during the config flow.
# We use the `error_on_register_user` mock instead of `bypass_get_data`
# (note the function parameters) to raise an Exception during
# validation of the input config.
async def test_failed_config_flow_registration(
    hass, enable_custom_integrations, error_on_register_user
):
    """Test a failed config flow due to credential validation failure."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_FORM
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {"base": "unable_to_register"}


# In this case, we want to simulate a failure during the config flow.
# We use the `error_on_get_data` mock instead of `bypass_get_data`
# (note the function parameters) to raise an Exception during
# validation of the input config.
async def test_failed_config_flow_verification(
    hass, enable_custom_integrations, error_on_get_data
):
    """Test a failed config flow due to credential validation failure."""

    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_FORM
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {"base": "auth"}


# Our config flow also has an options flow, so we must test it as well.
async def test_options_flow(hass, enable_custom_integrations, bypass_get_data):
    """Test an options flow."""
    # Create a new MockConfigEntry and add to HASS (we're bypassing config
    # flow entirely)
    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    entry.add_to_hass(hass)

    # Initialize an options flow
    await hass.config_entries.async_setup(entry.entry_id)
    result = await hass.config_entries.options.async_init(entry.entry_id)

    # Verify that the first options step is a user form
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "user"

    # Enter some fake data into the form
    form = {"test_allergen": True}
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input=form,
    )

    # Verify that the flow finishes
    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result["title"] == "test_app_id"

    # Verify that the options were updated
    assert entry.options == form


# Our config flow also has an options flow, so we must test it as well.
async def test_options_flow_with_options(
    hass, enable_custom_integrations, bypass_get_data
):
    """Test an options flow."""
    # Create a new MockConfigEntry and add to HASS (we're bypassing config
    # flow entirely)
    form = {"test_allergen": True}
    entry = MockConfigEntry(
        domain=DOMAIN, data=MOCK_CONFIG, entry_id="test", options=form
    )
    entry.add_to_hass(hass)

    # Initialize an options flow
    await hass.config_entries.async_setup(entry.entry_id)
    result = await hass.config_entries.options.async_init(entry.entry_id)

    # Verify that the first options step is a user form
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "user"

    # Enter some fake data into the form
    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input=form,
    )

    # Verify that the flow finishes
    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result["title"] == "test_app_id"

    # If all options are true, we store an empty dict
    assert entry.options == {}


async def test_failed_options_flow(hass, enable_custom_integrations, error_on_get_data):
    """Test an options flow."""
    # Create a new MockConfigEntry and add to HASS (we're bypassing config
    # flow entirely)
    entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    entry.add_to_hass(hass)

    # Initialize an options flow
    await hass.config_entries.async_setup(entry.entry_id)
    result = await hass.config_entries.options.async_init(entry.entry_id)

    # Verify that the first options step is a user form
    assert result["type"] == data_entry_flow.RESULT_TYPE_ABORT
    assert result["reason"] == "unable_to_fetch_data"
