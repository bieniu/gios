"""Tests for gios package."""

from typing import Any

import aiohttp
import pytest
from aioresponses import aioresponses
from syrupy import SnapshotAssertion

from gios import ApiError, Gios, InvalidSensorsDataError, NoStationError

INVALID_STATION_ID = 0

VALID_STATION_ID = 552
VALID_STATION_NAME = "Test Name"
VALID_LATITUDE = 99.99
VALID_LONGITUDE = 88.88


@pytest.mark.asyncio
async def test_init_only(
    session: aiohttp.ClientSession,
    session_mock: aioresponses,
    snapshot: SnapshotAssertion,
    stations: list[dict[str, Any]],
) -> None:
    """Test init without station."""
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/station/findAll",
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
    sensor_658: dict[str, Any],
    sensor_660: dict[str, Any],
    sensor_665: dict[str, Any],
    sensor_667: dict[str, Any],
    sensor_670: dict[str, Any],
    sensor_672: dict[str, Any],
    sensor_14395: dict[str, Any],
) -> None:
    """Test with valid data and valid first sensor's value."""
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/station/findAll",
        payload=stations,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/rest/station/sensors/{VALID_STATION_ID}",
        payload=station,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/672",
        payload=sensor_672,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/658",
        payload=sensor_658,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/660",
        payload=sensor_660,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/665",
        payload=sensor_665,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/667",
        payload=sensor_667,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/670",
        payload=sensor_670,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/14395",
        payload=sensor_14395,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{VALID_STATION_ID}",
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
        "https://api.gios.gov.pl/pjp-api/rest/station/findAll",
        status=404,
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
    sensor_658: dict[str, Any],
    sensor_660: dict[str, Any],
    sensor_665: dict[str, Any],
    sensor_667: dict[str, Any],
    sensor_670: dict[str, Any],
    sensor_672: dict[str, Any],
    sensor_14395: dict[str, Any],
) -> None:
    """Test with valid data and valid second sensor's value."""
    sensor_658["values"][0]["value"] = None
    sensor_660["values"][0]["value"] = None
    sensor_665["values"][0]["value"] = None
    sensor_667["values"][0]["value"] = None
    sensor_670["values"][0]["value"] = None
    sensor_672["values"][0]["value"] = None
    sensor_14395["values"][0]["value"] = None

    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/station/findAll",
        payload=stations,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/rest/station/sensors/{VALID_STATION_ID}",
        payload=station,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/672",
        payload=sensor_672,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/658",
        payload=sensor_658,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/660",
        payload=sensor_660,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/665",
        payload=sensor_665,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/667",
        payload=sensor_667,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/670",
        payload=sensor_670,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/14395",
        payload=sensor_14395,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{VALID_STATION_ID}",
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
    sensor_658: dict[str, Any],
    sensor_660: dict[str, Any],
    sensor_665: dict[str, Any],
    sensor_667: dict[str, Any],
    sensor_670: dict[str, Any],
    sensor_672: dict[str, Any],
    sensor_14395: dict[str, Any],
) -> None:
    """Test with valid data."""
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/station/findAll",
        payload=stations,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/rest/station/sensors/{VALID_STATION_ID}",
        payload=station,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/672",
        payload=sensor_672,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/658",
        payload=sensor_658,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/660",
        payload=sensor_660,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/665",
        payload=sensor_665,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/667",
        payload=sensor_667,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/670",
        payload=sensor_670,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/14395",
        payload=sensor_14395,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{VALID_STATION_ID}",
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
    sensor_658: dict[str, Any],
    sensor_660: dict[str, Any],
    sensor_665: dict[str, Any],
    sensor_667: dict[str, Any],
    sensor_670: dict[str, Any],
    sensor_672: dict[str, Any],
    sensor_14395: dict[str, Any],
) -> None:
    """Test with no sensor data."""
    sensor_658["values"][0]["value"] = None
    sensor_658["values"][1]["value"] = None
    sensor_660["values"][0]["value"] = None
    sensor_660["values"][1]["value"] = None
    sensor_665["values"][0]["value"] = None
    sensor_665["values"][1]["value"] = None
    sensor_667["values"][0]["value"] = None
    sensor_667["values"][1]["value"] = None
    sensor_670["values"][0]["value"] = None
    sensor_670["values"][1]["value"] = None
    sensor_672["values"][0]["value"] = None
    sensor_672["values"][1]["value"] = None
    sensor_14395["values"][0]["value"] = None
    sensor_14395["values"][1]["value"] = None

    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/station/findAll",
        payload=stations,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/rest/station/sensors/{VALID_STATION_ID}",
        payload=station,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/672",
        payload=sensor_672,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/658",
        payload=sensor_658,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/660",
        payload=sensor_660,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/665",
        payload=sensor_665,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/667",
        payload=sensor_667,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/670",
        payload=sensor_670,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/14395",
        payload=sensor_14395,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{VALID_STATION_ID}",
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
        "https://api.gios.gov.pl/pjp-api/rest/station/findAll",
        payload=stations,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/rest/station/sensors/{VALID_STATION_ID}",
        payload=station,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/672",
        payload=None,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/658",
        payload=None,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/660",
        payload=None,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/665",
        payload=None,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/667",
        payload=None,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/670",
        payload=None,
    )
    session_mock.get(
        "https://api.gios.gov.pl/pjp-api/rest/data/getData/14395",
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
        "https://api.gios.gov.pl/pjp-api/rest/station/findAll",
        payload=stations,
    )
    session_mock.get(
        f"https://api.gios.gov.pl/pjp-api/rest/station/sensors/{VALID_STATION_ID}",
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
        "https://api.gios.gov.pl/pjp-api/rest/station/findAll",
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
        "https://api.gios.gov.pl/pjp-api/rest/station/findAll",
        payload=stations,
    )

    with pytest.raises(NoStationError, match="0 is not a valid measuring station ID"):
        await Gios.create(session, INVALID_STATION_ID)
