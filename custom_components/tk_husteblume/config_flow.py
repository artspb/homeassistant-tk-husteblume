"""Adds config flow for TK Husteblume."""

import logging
import secrets

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_create_clientsession
from homeassistant.helpers.selector import SelectSelector
from homeassistant.helpers.selector import SelectSelectorConfig
from homeassistant.helpers.selector import SelectSelectorMode

from .api import TkHusteblumeApiClient
from .const import CONF_AGE_GROUP
from .const import CONF_APP_ID
from .const import CONF_BIRTH_MONTH
from .const import CONF_GENDER
from .const import CONF_PASSWORD
from .const import CONF_STATION
from .const import DOMAIN

_LOGGER: logging.Logger = logging.getLogger(__package__)


class TkHusteblumeFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for tk_husteblume."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            _LOGGER.info("Registering a new user")
            password = secrets.token_urlsafe(16)
            user = await self._register_user(
                user_input[CONF_AGE_GROUP],
                user_input[CONF_BIRTH_MONTH],
                user_input[CONF_GENDER],
                password,
            )

            if "appId" in user:
                _LOGGER.info("Successfully registered a new user")
                user_input[CONF_PASSWORD] = password
                user_input[CONF_APP_ID] = user["appId"]

                _LOGGER.info("Verifying credentials")
                valid = await self._test_credentials(
                    user_input[CONF_APP_ID],
                    user_input[CONF_PASSWORD],
                    user_input[CONF_STATION],
                )
                if valid:
                    _LOGGER.info("Credentials are valid, creating an entry")
                    return self.async_create_entry(
                        title=user_input[CONF_APP_ID], data=user_input
                    )
                else:
                    self._errors["base"] = "auth"
            else:
                self._errors["base"] = "unable_to_register"

        _LOGGER.info("Showing a config form")
        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):  # pylint: disable=unused-argument
        """Show the configuration form."""
        if user_input is None:
            user_input = {}

        stations = await self._get_stations()
        if not stations:
            return self.async_abort(reason="unable_to_fetch_stations")

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_AGE_GROUP, default=user_input.get(CONF_AGE_GROUP)
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=[
                                "UP_TO_TWENTY",
                                "TWENTY_ONE_TO_FORTY",
                                "FORTY_ONE_AND_ABOVE",
                            ],
                            mode=SelectSelectorMode.DROPDOWN,
                            translation_key=CONF_AGE_GROUP,
                        ),
                    ),
                    vol.Required(
                        CONF_GENDER, default=user_input.get(CONF_GENDER)
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=["MALE", "FEMALE", "OTHER"],
                            mode=SelectSelectorMode.DROPDOWN,
                            translation_key=CONF_GENDER,
                        ),
                    ),
                    vol.Required(
                        CONF_BIRTH_MONTH, default=user_input.get(CONF_BIRTH_MONTH)
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=[str(i) for i in range(1, 13)],
                            mode=SelectSelectorMode.DROPDOWN,
                            translation_key=CONF_BIRTH_MONTH,
                        ),
                    ),
                    vol.Required(
                        CONF_STATION, default=user_input.get(CONF_STATION)
                    ): SelectSelector(
                        SelectSelectorConfig(
                            options=list(stations.keys()),
                            mode=SelectSelectorMode.DROPDOWN,
                            translation_key=CONF_STATION,
                        ),
                    ),
                }
            ),
            errors=self._errors,
        )

    async def _get_stations(self):
        """Obtain a list of stations."""
        try:
            session = async_create_clientsession(self.hass)
            client = TkHusteblumeApiClient(session)
            return await client.async_get_stations()
        except Exception as e:  # pylint: disable=broad-except
            _LOGGER.error("Unable to fetch stations", e)
            return None

    async def _register_user(self, age_group, birth_month, gender, password):
        """Register a new user."""
        try:
            session = async_create_clientsession(self.hass)
            client = TkHusteblumeApiClient(session)
            return await client.async_register_user(
                age_group, birth_month, gender, password
            )
        except Exception as e:  # pylint: disable=broad-except
            _LOGGER.error("Unable to register a new user", e)
            return None

    async def _test_credentials(self, app_id, password, station):
        """Verify credentials."""
        try:
            session = async_create_clientsession(self.hass)
            client = TkHusteblumeApiClient(session, app_id, password, station)
            await client.async_get_data()
            return True
        except Exception as e:  # pylint: disable=broad-except
            _LOGGER.error("Invalid credentials", e)
            return False
