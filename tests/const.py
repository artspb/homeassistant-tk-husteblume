"""Constants for TK Husteblume tests."""

from custom_components.tk_husteblume import CONF_STATION
from custom_components.tk_husteblume.const import CONF_AGE_GROUP
from custom_components.tk_husteblume.const import CONF_APP_ID
from custom_components.tk_husteblume.const import CONF_BIRTH_MONTH
from custom_components.tk_husteblume.const import CONF_GENDER
from custom_components.tk_husteblume.const import CONF_PASSWORD

MOCK_FORM = {
    CONF_AGE_GROUP: "up_to_twenty",
    CONF_GENDER: "male",
    CONF_BIRTH_MONTH: "1",
    CONF_STATION: "test_station",
}

MOCK_CONFIG = MOCK_FORM | {
    CONF_APP_ID: "test_app_id",
    CONF_PASSWORD: "test_password",
    CONF_STATION: "test_station",
}
