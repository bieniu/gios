"""Tests for gios package."""

from http import HTTPStatus
from typing import Any

import aiohttp
import pytest
from aioresponses import aioresponses
from syrupy import SnapshotAssertion

from gios import ApiError, Gios, InvalidSensorsDataError, NoStationError

INVALID_STATION_ID = 0

VALID_STATION_ID = 552
VALID_STATION_NAME = "Warszawa, ul. Kondratowicza"
VALID_LATITUDE = 52.290864
VALID_LONGITUDE = 21.042458


@pytest.mark.asyncio
async def test_init_only(
    session: aiohttp.ClientSession,
    session_mock: aioresponses,
    snapshot: SnapshotAssertion,
    stations: list[dict[str, Any]],
) -> None:
    """Test init without station."""
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?page=0&size=1000",
        payload=stations,
    )

    gios = await Gios.create(session)

    with pytest.raises(NoStationError, match="Measuring station ID is not set"):
        await gios.async_update()

    assert gios.station_name is None
    assert gios.station_id is None
    assert gios.latitude is None
    assert gios.longitude is None
    assert gios.measurement_stations == snapshot


@pytest.mark.asyncio
async def test_valid_data_first_value(
    session: aiohttp.ClientSession,
    session_mock: aioresponses,
    snapshot: SnapshotAssertion,
    stations: list[dict[str, Any]],
    station: list[dict[str, Any]],
    indexes: dict[str, Any],
    sensor_3759: dict[str, Any],
    sensor_3760: dict[str, Any],
    sensor_3761: dict[str, Any],
    sensor_3762: dict[str, Any],
    sensor_3764: dict[str, Any],
    sensor_3765: dict[str, Any],
    sensor_14688: dict[str, Any],
) -> None:
    """Test with valid data and valid first sensor's value."""
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?page=0&size=1000",
        payload=stations,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/{VALID_STATION_ID}",
        payload=station,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3759",
        payload=sensor_3759,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3760",
        payload=sensor_3760,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3761",
        payload=sensor_3761,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3762",
        payload=sensor_3762,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3764",
        payload=sensor_3764,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3765",
        payload=sensor_3765,
        status=HTTPStatus.BAD_REQUEST.value,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/14688",
        payload=sensor_14688,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/v1/rest/aqindex/getIndex/{VALID_STATION_ID}",
        payload=indexes,
    )

    gios = await Gios.create(session, VALID_STATION_ID)
    data = await gios.async_update()

    assert gios.station_name == VALID_STATION_NAME
    assert gios.station_id == VALID_STATION_ID
    assert gios.latitude == VALID_LATITUDE
    assert gios.longitude == VALID_LONGITUDE
    assert gios.measurement_stations == snapshot
    assert data == snapshot


@pytest.mark.asyncio
async def test_api_error(
    session: aiohttp.ClientSession, session_mock: aioresponses
) -> None:
    """Test GIOS API error."""
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?page=0&size=1000",
        status=HTTPStatus.NOT_FOUND.value,
    )

    with pytest.raises(ApiError) as excinfo:
        await Gios.create(session, VALID_STATION_ID)

    assert str(excinfo.value) == "404"


@pytest.mark.asyncio
async def test_valid_data_second_value(
    session: aiohttp.ClientSession,
    session_mock: aioresponses,
    snapshot: SnapshotAssertion,
    stations: list[dict[str, Any]],
    station: list[dict[str, Any]],
    indexes: dict[str, Any],
    sensor_3759: dict[str, Any],
    sensor_3760: dict[str, Any],
    sensor_3761: dict[str, Any],
    sensor_3762: dict[str, Any],
    sensor_3764: dict[str, Any],
    sensor_3765: dict[str, Any],
    sensor_14688: dict[str, Any],
) -> None:
    """Test with valid data and valid second sensor's value."""
    sensor_3760["Lista danych pomiarowych"][0]["Wartość"] = None
    sensor_3761["Lista danych pomiarowych"][0]["Wartość"] = None
    sensor_3762["Lista danych pomiarowych"][0]["Wartość"] = None
    sensor_3764["Lista danych pomiarowych"][0]["Wartość"] = None

    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?page=0&size=1000",
        payload=stations,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/{VALID_STATION_ID}",
        payload=station,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3759",
        payload=sensor_3759,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3760",
        payload=sensor_3760,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3761",
        payload=sensor_3761,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3762",
        payload=sensor_3762,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3764",
        payload=sensor_3764,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3765",
        payload=sensor_3765,
        status=HTTPStatus.BAD_REQUEST.value,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/14688",
        payload=sensor_14688,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/v1/rest/aqindex/getIndex/{VALID_STATION_ID}",
        payload=indexes,
    )

    gios = await Gios.create(session, VALID_STATION_ID)
    data = await gios.async_update()

    assert gios.station_name == VALID_STATION_NAME
    assert gios.station_id == VALID_STATION_ID
    assert gios.latitude == VALID_LATITUDE
    assert gios.longitude == VALID_LONGITUDE
    assert gios.measurement_stations == snapshot
    assert data == snapshot


@pytest.mark.asyncio
async def test_no_indexes_data(
    session: aiohttp.ClientSession,
    session_mock: aioresponses,
    snapshot: SnapshotAssertion,
    stations: list[dict[str, Any]],
    station: list[dict[str, Any]],
    sensor_3759: dict[str, Any],
    sensor_3760: dict[str, Any],
    sensor_3761: dict[str, Any],
    sensor_3762: dict[str, Any],
    sensor_3764: dict[str, Any],
    sensor_3765: dict[str, Any],
    sensor_14688: dict[str, Any],
) -> None:
    """Test with valid data."""
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?page=0&size=1000",
        payload=stations,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/{VALID_STATION_ID}",
        payload=station,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3759",
        payload=sensor_3759,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3760",
        payload=sensor_3760,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3761",
        payload=sensor_3761,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3762",
        payload=sensor_3762,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3764",
        payload=sensor_3764,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3765",
        payload=sensor_3765,
        status=HTTPStatus.BAD_REQUEST.value,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/14688",
        payload=sensor_14688,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/v1/rest/aqindex/getIndex/{VALID_STATION_ID}",
        payload={},
    )

    gios = await Gios.create(session, VALID_STATION_ID)
    data = await gios.async_update()

    assert gios.station_name == VALID_STATION_NAME
    assert gios.station_id == VALID_STATION_ID
    assert gios.latitude == VALID_LATITUDE
    assert gios.longitude == VALID_LONGITUDE
    assert gios.measurement_stations == snapshot
    assert data == snapshot


@pytest.mark.asyncio
async def test_no_sensor_data_1(
    session: aiohttp.ClientSession,
    session_mock: aioresponses,
    stations: list[dict[str, Any]],
    station: list[dict[str, Any]],
    indexes: dict[str, Any],
    sensor_3759: dict[str, Any],
    sensor_3760: dict[str, Any],
    sensor_3761: dict[str, Any],
    sensor_3762: dict[str, Any],
    sensor_3764: dict[str, Any],
    sensor_3765: dict[str, Any],
    sensor_14688: dict[str, Any],
) -> None:
    """Test with no sensor data."""
    sensor_3759["Lista danych pomiarowych"][0]["Wartość"] = None
    sensor_3759["Lista danych pomiarowych"][1]["Wartość"] = None
    sensor_3760["Lista danych pomiarowych"][0]["Wartość"] = None
    sensor_3760["Lista danych pomiarowych"][1]["Wartość"] = None
    sensor_3761["Lista danych pomiarowych"][0]["Wartość"] = None
    sensor_3761["Lista danych pomiarowych"][1]["Wartość"] = None
    sensor_3762["Lista danych pomiarowych"][0]["Wartość"] = None
    sensor_3762["Lista danych pomiarowych"][1]["Wartość"] = None
    sensor_3764["Lista danych pomiarowych"][0]["Wartość"] = None
    sensor_3764["Lista danych pomiarowych"][1]["Wartość"] = None
    sensor_14688["Lista danych pomiarowych"][0]["Wartość"] = None
    sensor_14688["Lista danych pomiarowych"][1]["Wartość"] = None

    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?page=0&size=1000",
        payload=stations,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/{VALID_STATION_ID}",
        payload=station,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3759",
        payload=sensor_3759,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3760",
        payload=sensor_3760,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3761",
        payload=sensor_3761,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3762",
        payload=sensor_3762,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3764",
        payload=sensor_3764,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3765",
        payload=sensor_3765,
        status=HTTPStatus.BAD_REQUEST.value,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/14688",
        payload=sensor_14688,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/v1/rest/aqindex/getIndex/{VALID_STATION_ID}",
        payload=indexes,
    )
    gios = await Gios.create(session, VALID_STATION_ID)

    with pytest.raises(
        InvalidSensorsDataError, match="Invalid sensor data from GIOS API"
    ):
        await gios.async_update()


@pytest.mark.asyncio
async def test_invalid_sensor_data_2(
    session: aiohttp.ClientSession,
    session_mock: aioresponses,
    stations: list[dict[str, Any]],
    station: list[dict[str, Any]],
) -> None:
    """Test with invalid sensor data."""
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?page=0&size=1000",
        payload=stations,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/{VALID_STATION_ID}",
        payload=station,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3759",
        payload=None,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3760",
        payload=None,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3761",
        payload=None,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3762",
        payload=None,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3764",
        payload=None,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3765",
        payload=None,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/14688",
        payload=None,
    )
    gios = await Gios.create(session, VALID_STATION_ID)

    with pytest.raises(
        InvalidSensorsDataError, match="Invalid sensor data from GIOS API"
    ):
        await gios.async_update()


@pytest.mark.asyncio
async def test_no_station_data(
    session: aiohttp.ClientSession,
    session_mock: aioresponses,
    stations: list[dict[str, Any]],
) -> None:
    """Test with no station data."""
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?page=0&size=1000",
        payload=stations,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/{VALID_STATION_ID}",
        payload={},
    )
    gios = await Gios.create(session, VALID_STATION_ID)

    with pytest.raises(
        InvalidSensorsDataError,
        match="Invalid measuring station data from GIOS API",
    ):
        await gios.async_update()


@pytest.mark.asyncio
async def test_no_stations_data(
    session: aiohttp.ClientSession, session_mock: aioresponses
) -> None:
    """Test with no stations data."""
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?page=0&size=1000",
        payload={},
    )

    with pytest.raises(NoStationError, match="552 is not a valid measuring station ID"):
        await Gios.create(session, VALID_STATION_ID)


@pytest.mark.asyncio
async def test_invalid_station_id(
    session: aiohttp.ClientSession,
    session_mock: aioresponses,
    stations: list[dict[str, Any]],
) -> None:
    """Test with invalid station_id."""
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?page=0&size=1000",
        payload=stations,
    )

    with pytest.raises(NoStationError, match="0 is not a valid measuring station ID"):
        await Gios.create(session, INVALID_STATION_ID)


@pytest.mark.asyncio
async def test_no_common_index(
    session: aiohttp.ClientSession,
    session_mock: aioresponses,
    stations: list[dict[str, Any]],
    station: list[dict[str, Any]],
    indexes: dict[str, Any],
    sensor_3759: dict[str, Any],
    sensor_3760: dict[str, Any],
    sensor_3761: dict[str, Any],
    sensor_3762: dict[str, Any],
    sensor_3764: dict[str, Any],
    sensor_3765: dict[str, Any],
    sensor_14688: dict[str, Any],
) -> None:
    """Test with valid data and valid first sensor's value."""
    indexes["AqIndex"]["Nazwa kategorii indeksu"] = "Brak indeksu"
    indexes["AqIndex"]["Status indeksu ogólnego dla stacji pomiarowej"] = False

    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?page=0&size=1000",
        payload=stations,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/{VALID_STATION_ID}",
        payload=station,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3759",
        payload=sensor_3759,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3760",
        payload=sensor_3760,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3761",
        payload=sensor_3761,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3762",
        payload=sensor_3762,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3764",
        payload=sensor_3764,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/3765",
        payload=sensor_3765,
        status=HTTPStatus.BAD_REQUEST.value,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/14688",
        payload=sensor_14688,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/v1/rest/aqindex/getIndex/{VALID_STATION_ID}",
        payload=indexes,
    )

    gios = await Gios.create(session, VALID_STATION_ID)
    data = await gios.async_update()

    assert data.aqi is None
