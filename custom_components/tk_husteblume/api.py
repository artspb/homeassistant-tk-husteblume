"""Sample API Client."""

import asyncio
import base64
import logging
import socket

import aiohttp
import async_timeout

TIMEOUT = 10


_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class TkHusteblumeApiClient:
    def __init__(
        self,
        session: aiohttp.ClientSession,
        app_id: str = "",
        password: str = "",
        station: str = "",
    ) -> None:
        """Sample API Client."""
        self._session = session
        self._app_id = app_id
        self._password = password
        self._station = station.upper()

    async def async_get_stations(self) -> dict:
        """Get data from the API."""
        url = "https://api.husteblume-app.de/locations?locationType=STATIONS"
        return await self.api_wrapper("get", url)

    async def async_register_user(
        self, age_group, birth_month, gender, password
    ) -> dict:
        """Get data from the API."""
        url = "https://api.husteblume-app.de/users"
        return await self.api_wrapper(
            "post",
            url,
            data={
                "age_group": age_group,
                "birth_month": birth_month,
                "gender": gender,
                "pwd": password,
            },
        )

    async def async_get_data(self) -> dict:
        """Get data from the API."""
        url = "https://api.husteblume-app.de/forecast/" + self._station
        headers = {
            "authorization": "Basic "
            + (
                base64.b64encode(f"{self._app_id}:{self._password}".encode("ascii"))
            ).decode("ascii")
        }
        return await self.api_wrapper("get", url, headers=headers)

    async def api_wrapper(self, method: str, url: str, data=None, headers=None) -> dict:
        """Get information from the API."""
        if data is None:
            data = {}
        if headers is None:
            headers = {}
        try:
            async with async_timeout.timeout(TIMEOUT):
                if method == "get":
                    response = await self._session.get(url, headers=headers)
                    return await response.json()

                elif method == "post":
                    response = await self._session.post(url, headers=headers, json=data)
                    return await response.json()

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)
