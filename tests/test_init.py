"""Tests for gios package."""
import json

import aiohttp
import pytest
from aioresponses import aioresponses

from gios import ApiError, Gios, InvalidSensorsDataError, NoStationError

INVALID_STATION_ID = 0

VALID_STATION_ID = 552
VALID_STATION_NAME = "Test Name"
VALID_LATITUDE = 99.99
VALID_LONGITUDE = 88.88


@pytest.mark.asyncio
async def test_valid_data_first_value():
    """Test with valid data and valid first sensor's value."""
    with open("tests/fixtures/stations.json", encoding="utf-8") as file:
        stations = json.load(file)
    with open("tests/fixtures/station.json", encoding="utf-8") as file:
        station = json.load(file)
    with open("tests/fixtures/sensor_658.json", encoding="utf-8") as file:
        sensor_658 = json.load(file)
    with open("tests/fixtures/sensor_660.json", encoding="utf-8") as file:
        sensor_660 = json.load(file)
    with open("tests/fixtures/sensor_665.json", encoding="utf-8") as file:
        sensor_665 = json.load(file)
    with open("tests/fixtures/sensor_667.json", encoding="utf-8") as file:
        sensor_667 = json.load(file)
    with open("tests/fixtures/sensor_670.json", encoding="utf-8") as file:
        sensor_670 = json.load(file)
    with open("tests/fixtures/sensor_672.json", encoding="utf-8") as file:
        sensor_672 = json.load(file)
    with open("tests/fixtures/sensor_14395.json", encoding="utf-8") as file:
        sensor_14395 = json.load(file)
    with open("tests/fixtures/indexes.json", encoding="utf-8") as file:
        indexes = json.load(file)

    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/station/findAll",
            payload=stations,
        )
        session_mock.get(
            f"http://api.gios.gov.pl/pjp-api/rest/station/sensors/{VALID_STATION_ID}",
            payload=station,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/672",
            payload=sensor_672,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/658",
            payload=sensor_658,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/660",
            payload=sensor_660,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/665",
            payload=sensor_665,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/667",
            payload=sensor_667,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/670",
            payload=sensor_670,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/14395",
            payload=sensor_14395,
        )
        session_mock.get(
            f"http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{VALID_STATION_ID}",
            payload=indexes,
        )

        gios = Gios(VALID_STATION_ID, session)
        data = await gios.async_update()

    await session.close()

    assert gios.station_name == VALID_STATION_NAME
    assert gios.station_id == VALID_STATION_ID
    assert gios.latitude == VALID_LATITUDE
    assert gios.longitude == VALID_LONGITUDE
    assert data.so2.value == 11.6502
    assert data.so2.index == "very_good"
    assert data.c6h6.value == 2.57148
    assert data.c6h6.index == "very_good"
    assert data.co.value == 786.702
    assert data.co.index == "very_bad"
    assert data.no2.value == 59.9545
    assert data.no2.index == "very_good"
    assert data.o3.value == 8.63111
    assert data.o3.index == "bad"
    assert data.pm25.value == 59.9428
    assert data.pm25.index == "sufficient"
    assert data.pm10.value == 123.879
    assert data.pm10.index == "moderate"
    assert data.aqi.value == "good"


@pytest.mark.asyncio
async def test_api_error():
    """Test GIOS API error."""
    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/station/findAll",
            status=404,
        )
        gios = Gios(VALID_STATION_ID, session)

        with pytest.raises(ApiError) as excinfo:
            await gios.async_update()

        assert str(excinfo.value) == "404"

    await session.close()


@pytest.mark.asyncio
async def test_valid_data_second_value():
    """Test with valid data and valid second sensor's value."""
    with open("tests/fixtures/stations.json", encoding="utf-8") as file:
        stations = json.load(file)
    with open("tests/fixtures/station.json", encoding="utf-8") as file:
        station = json.load(file)
    with open("tests/fixtures/sensor_658.json", encoding="utf-8") as file:
        sensor_658 = json.load(file)
    with open("tests/fixtures/sensor_660.json", encoding="utf-8") as file:
        sensor_660 = json.load(file)
    with open("tests/fixtures/sensor_665.json", encoding="utf-8") as file:
        sensor_665 = json.load(file)
    with open("tests/fixtures/sensor_667.json", encoding="utf-8") as file:
        sensor_667 = json.load(file)
    with open("tests/fixtures/sensor_670.json", encoding="utf-8") as file:
        sensor_670 = json.load(file)
    with open("tests/fixtures/sensor_672.json", encoding="utf-8") as file:
        sensor_672 = json.load(file)
    with open("tests/fixtures/sensor_14395.json", encoding="utf-8") as file:
        sensor_14395 = json.load(file)
    with open("tests/fixtures/indexes.json", encoding="utf-8") as file:
        indexes = json.load(file)

    sensor_658["values"][0]["value"] = None
    sensor_660["values"][0]["value"] = None
    sensor_665["values"][0]["value"] = None
    sensor_667["values"][0]["value"] = None
    sensor_670["values"][0]["value"] = None
    sensor_672["values"][0]["value"] = None
    sensor_14395["values"][0]["value"] = None

    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/station/findAll",
            payload=stations,
        )
        session_mock.get(
            f"http://api.gios.gov.pl/pjp-api/rest/station/sensors/{VALID_STATION_ID}",
            payload=station,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/672",
            payload=sensor_672,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/658",
            payload=sensor_658,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/660",
            payload=sensor_660,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/665",
            payload=sensor_665,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/667",
            payload=sensor_667,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/670",
            payload=sensor_670,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/14395",
            payload=sensor_14395,
        )
        session_mock.get(
            f"http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{VALID_STATION_ID}",
            payload=indexes,
        )

        gios = Gios(VALID_STATION_ID, session)
        data = await gios.async_update()

    await session.close()

    assert gios.station_name == VALID_STATION_NAME
    assert gios.station_id == VALID_STATION_ID
    assert gios.latitude == VALID_LATITUDE
    assert gios.longitude == VALID_LONGITUDE
    assert data.so2.value == 11.501
    assert data.so2.index == "very_good"
    assert data.c6h6.value == 3.24432
    assert data.c6h6.index == "very_good"
    assert data.co.value == 1041.74
    assert data.co.index == "very_bad"
    assert data.no2.value == 52.6198
    assert data.no2.index == "very_good"
    assert data.o3.value == 4.93778
    assert data.o3.index == "bad"
    assert data.pm25.value == 72.0243
    assert data.pm25.index == "sufficient"
    assert data.pm10.value == 115.559
    assert data.pm10.index == "moderate"
    assert data.aqi.value == "good"


@pytest.mark.asyncio
async def test_no_indexes_data():
    """Test with valid data."""
    with open("tests/fixtures/stations.json", encoding="utf-8") as file:
        stations = json.load(file)
    with open("tests/fixtures/station.json", encoding="utf-8") as file:
        station = json.load(file)
    with open("tests/fixtures/sensor_658.json", encoding="utf-8") as file:
        sensor_658 = json.load(file)
    with open("tests/fixtures/sensor_660.json", encoding="utf-8") as file:
        sensor_660 = json.load(file)
    with open("tests/fixtures/sensor_665.json", encoding="utf-8") as file:
        sensor_665 = json.load(file)
    with open("tests/fixtures/sensor_667.json", encoding="utf-8") as file:
        sensor_667 = json.load(file)
    with open("tests/fixtures/sensor_670.json", encoding="utf-8") as file:
        sensor_670 = json.load(file)
    with open("tests/fixtures/sensor_672.json", encoding="utf-8") as file:
        sensor_672 = json.load(file)
    with open("tests/fixtures/sensor_14395.json", encoding="utf-8") as file:
        sensor_14395 = json.load(file)

    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/station/findAll",
            payload=stations,
        )
        session_mock.get(
            f"http://api.gios.gov.pl/pjp-api/rest/station/sensors/{VALID_STATION_ID}",
            payload=station,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/672",
            payload=sensor_672,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/658",
            payload=sensor_658,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/660",
            payload=sensor_660,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/665",
            payload=sensor_665,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/667",
            payload=sensor_667,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/670",
            payload=sensor_670,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/14395",
            payload=sensor_14395,
        )
        session_mock.get(
            f"http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{VALID_STATION_ID}",
            payload={},
        )

        gios = Gios(VALID_STATION_ID, session)
        data = await gios.async_update()

    await session.close()

    assert gios.station_name == VALID_STATION_NAME
    assert gios.station_id == VALID_STATION_ID
    assert gios.latitude == VALID_LATITUDE
    assert gios.longitude == VALID_LONGITUDE
    assert data.so2.value == 11.6502
    assert data.so2.index is None
    assert data.c6h6.value == 2.57148
    assert data.c6h6.index is None
    assert data.co.value == 786.702
    assert data.co.index is None
    assert data.no2.value == 59.9545
    assert data.no2.index is None
    assert data.o3.value == 8.63111
    assert data.o3.index is None
    assert data.pm25.value == 59.9428
    assert data.pm25.index is None
    assert data.pm10.value == 123.879
    assert data.pm10.index is None
    assert data.aqi is None


@pytest.mark.asyncio
async def test_no_sensor_data_1():
    """Test with no sensor data."""
    with open("tests/fixtures/stations.json", encoding="utf-8") as file:
        stations = json.load(file)
    with open("tests/fixtures/station.json", encoding="utf-8") as file:
        station = json.load(file)
    with open("tests/fixtures/sensor_658.json", encoding="utf-8") as file:
        sensor_658 = json.load(file)
    with open("tests/fixtures/sensor_660.json", encoding="utf-8") as file:
        sensor_660 = json.load(file)
    with open("tests/fixtures/sensor_665.json", encoding="utf-8") as file:
        sensor_665 = json.load(file)
    with open("tests/fixtures/sensor_667.json", encoding="utf-8") as file:
        sensor_667 = json.load(file)
    with open("tests/fixtures/sensor_670.json", encoding="utf-8") as file:
        sensor_670 = json.load(file)
    with open("tests/fixtures/sensor_672.json", encoding="utf-8") as file:
        sensor_672 = json.load(file)
    with open("tests/fixtures/sensor_14395.json", encoding="utf-8") as file:
        sensor_14395 = json.load(file)
    with open("tests/fixtures/indexes.json", encoding="utf-8") as file:
        indexes = json.load(file)

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

    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/station/findAll",
            payload=stations,
        )
        session_mock.get(
            f"http://api.gios.gov.pl/pjp-api/rest/station/sensors/{VALID_STATION_ID}",
            payload=station,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/672",
            payload=sensor_672,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/658",
            payload=sensor_658,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/660",
            payload=sensor_660,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/665",
            payload=sensor_665,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/667",
            payload=sensor_667,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/670",
            payload=sensor_670,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/14395",
            payload=sensor_14395,
        )
        session_mock.get(
            f"http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{VALID_STATION_ID}",
            payload=indexes,
        )
        gios = Gios(VALID_STATION_ID, session)

        with pytest.raises(InvalidSensorsDataError):
            await gios.async_update()

    await session.close()


@pytest.mark.asyncio
async def test_invalid_sensor_data_2():
    """Test with invalid sensor data."""
    with open("tests/fixtures/stations.json", encoding="utf-8") as file:
        stations = json.load(file)
    with open("tests/fixtures/station.json", encoding="utf-8") as file:
        station = json.load(file)

    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/station/findAll",
            payload=stations,
        )
        session_mock.get(
            f"http://api.gios.gov.pl/pjp-api/rest/station/sensors/{VALID_STATION_ID}",
            payload=station,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/672",
            payload=None,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/658",
            payload=None,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/660",
            payload=None,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/665",
            payload=None,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/667",
            payload=None,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/670",
            payload=None,
        )
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/data/getData/14395",
            payload=None,
        )
        gios = Gios(VALID_STATION_ID, session)

        with pytest.raises(InvalidSensorsDataError):
            await gios.async_update()

    await session.close()


@pytest.mark.asyncio
async def test_no_station_data():
    """Test with no station data."""
    with open("tests/fixtures/stations.json", encoding="utf-8") as file:
        stations = json.load(file)

    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/station/findAll",
            payload=stations,
        )
        session_mock.get(
            f"http://api.gios.gov.pl/pjp-api/rest/station/sensors/{VALID_STATION_ID}",
            payload={},
        )
        gios = Gios(VALID_STATION_ID, session)

        with pytest.raises(InvalidSensorsDataError):
            await gios.async_update()

    await session.close()


@pytest.mark.asyncio
async def test_no_stations_data():
    """Test with no stations data."""
    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/station/findAll",
            payload={},
        )
        gios = Gios(VALID_STATION_ID, session)

        with pytest.raises(ApiError):
            await gios.async_update()

    await session.close()


@pytest.mark.asyncio
async def test_invalid_station_id():
    """Test with invalid station_id."""
    with open("tests/fixtures/stations.json", encoding="utf-8") as file:
        stations = json.load(file)

    session = aiohttp.ClientSession()

    with aioresponses() as session_mock:
        session_mock.get(
            "http://api.gios.gov.pl/pjp-api/rest/station/findAll",
            payload=stations,
        )
        gios = Gios(INVALID_STATION_ID, session)

        with pytest.raises(NoStationError) as excinfo:
            await gios.async_update()

        assert str(excinfo.value) == "0 is not a valid measuring station ID"

    await session.close()
