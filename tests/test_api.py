"""Tests for TK Husteblume api."""

import asyncio

import aiohttp
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from yarl import URL

from custom_components.tk_husteblume.api import TkHusteblumeApiClient


async def test_api(hass, aioclient_mock, caplog):
    """Test API calls."""

    # To test the api submodule, we first create an instance of our API client
    api = TkHusteblumeApiClient(
        async_get_clientsession(hass), "test_app_id", "test_password", "test_station"
    )

    # Use aioclient_mock which is provided by `pytest_homeassistant_custom_components`
    # to mock responses to aiohttp requests. In this case we are telling the mock to
    # return {"test": "test"} when a `GET` call is made to the specified URL. We then
    # call `async_get_stations` which will make that `GET` request.
    result = {"test": "test"}
    aioclient_mock.clear_requests()
    aioclient_mock.get(
        "https://api.husteblume-app.de/locations?locationType=STATIONS", json=result
    )
    assert await api.async_get_stations() == result
    assert aioclient_mock.call_count == 1

    aioclient_mock.clear_requests()
    aioclient_mock.post("https://api.husteblume-app.de/users", json=result)
    assert (
        await api.async_register_user(
            "test_age_group", "test_birth_month", "test_gender", "test_password"
        )
        == result
    )
    assert aioclient_mock.call_count == 1
    assert aioclient_mock.mock_calls[0] == (
        "POST",
        URL("https://api.husteblume-app.de/users"),
        {
            "age_group": "test_age_group",
            "birth_month": "test_birth_month",
            "gender": "test_gender",
            "pwd": "test_password",
        },
        {},
    )

    aioclient_mock.clear_requests()
    aioclient_mock.get(
        "https://api.husteblume-app.de/forecast/test_station", json=result
    )
    assert await api.async_get_data() == result
    assert aioclient_mock.call_count == 1
    assert aioclient_mock.mock_calls[0] == (
        "GET",
        URL("https://api.husteblume-app.de/forecast/test_station"),
        None,
        {"authorization": "Basic dGVzdF9hcHBfaWQ6dGVzdF9wYXNzd29yZA=="},
    )

    # In order to get 100% coverage, we need to test `api_wrapper` to test the code
    # that isn't already called by `async_get_stations` and `async_get_data`.
    # Because the only logic that lives inside `api_wrapper` that is not being handled by a third
    # party library (aiohttp) is the exception handling, we also want to simulate
    # raising the exceptions to ensure that the function handles them as expected.
    # The caplog fixture allows access to log messages in tests.
    # This is particularly
    # useful during exception handling testing since often the only action as part of
    # exception handling is a logging statement
    caplog.clear()
    aioclient_mock.get(
        "https://jsonplaceholder.typicode.com/posts/1", exc=asyncio.TimeoutError
    )
    assert (
        await api.api_wrapper("get", "https://jsonplaceholder.typicode.com/posts/1")
        is None
    )
    assert (
        len(caplog.record_tuples) == 1
        and "Timeout error fetching information from" in caplog.record_tuples[0][2]
    )

    caplog.clear()
    aioclient_mock.post(
        "https://jsonplaceholder.typicode.com/posts/1", exc=aiohttp.ClientError
    )
    assert (
        await api.api_wrapper("post", "https://jsonplaceholder.typicode.com/posts/1")
        is None
    )
    assert (
        len(caplog.record_tuples) == 1
        and "Error fetching information from" in caplog.record_tuples[0][2]
    )

    caplog.clear()
    aioclient_mock.post("https://jsonplaceholder.typicode.com/posts/2", exc=Exception)
    assert (
        await api.api_wrapper("post", "https://jsonplaceholder.typicode.com/posts/2")
        is None
    )
    assert (
        len(caplog.record_tuples) == 1
        and "Something really wrong happened!" in caplog.record_tuples[0][2]
    )

    caplog.clear()
    aioclient_mock.post("https://jsonplaceholder.typicode.com/posts/3", exc=TypeError)
    assert (
        await api.api_wrapper("post", "https://jsonplaceholder.typicode.com/posts/3")
        is None
    )
    assert (
        len(caplog.record_tuples) == 1
        and "Error parsing information from" in caplog.record_tuples[0][2]
    )
