"""Constants for TK Husteblume."""

# Base component constants
NAME = "TK Husteblume"
DOMAIN = "tk_husteblume"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.7"

ATTRIBUTION = "Data provided by Techniker Krankenkasse"
ISSUE_URL = "https://github.com/artspb/homeassistant-tk-husteblume/issues"

# Icons
ICON = "mdi:allergy"

# Platforms
SENSOR = "sensor"
PLATFORMS = [SENSOR]


# Configuration and options
CONF_AGE_GROUP = "age_group"
CONF_GENDER = "gender"
CONF_BIRTH_MONTH = "birth_month"
CONF_STATION = "station"
CONF_APP_ID = "app_id"
CONF_PASSWORD = "password"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
