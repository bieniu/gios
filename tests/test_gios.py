import asyncio
import json

import pytest
from aiohttp import ClientSession
from asynctest import patch

import pygios

INVALID_STATION_ID = 0

NO_MEASURING_STATION = f"{INVALID_STATION_ID} is not a valid measuring station ID."

TEST_STATION_ID = 552
TEST_STATION_NAME = "Test Name"
TEST_LATITUDE = "99.99"
TEST_LONGITUDE = "88.88"
TEST_AQI_VALUE = "good"
TEST_PM10_VALUE = 11.11


@pytest.mark.asyncio
async def test_valid_data():
    """Test with valid data."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with open("tests/data/station.json") as file:
        station = json.load(file)

    with open("tests/data/sensor.json") as file:
        sensor = json.load(file)

    with open("tests/data/indexes.json") as file:
        indexes = json.load(file)

    with patch("pygios.Gios._get_stations", return_value=stations), patch(
        "pygios.Gios._get_station", return_value=station
    ), patch("pygios.Gios._get_sensor", return_value=sensor), patch(
        "pygios.Gios._get_indexes", return_value=indexes
    ):
        async with ClientSession() as websession:
            gios = pygios.Gios(TEST_STATION_ID, websession)
            await gios.update()

        assert gios.station_name == TEST_STATION_NAME
        assert gios.latitude == TEST_LATITUDE
        assert gios.longitude == TEST_LONGITUDE
        assert gios.available == True
        assert len(gios.data) == 2
        assert gios.data["PM10"]["value"] == TEST_PM10_VALUE
        assert gios.data["AQI"]["value"] == TEST_AQI_VALUE


@pytest.mark.asyncio
async def test_invalid_indexes_data():
    """Test with valid data."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with open("tests/data/station.json") as file:
        station = json.load(file)

    with open("tests/data/sensor.json") as file:
        sensor = json.load(file)

    indexes = {}

    with patch("pygios.Gios._get_stations", return_value=stations), patch(
        "pygios.Gios._get_station", return_value=station
    ), patch("pygios.Gios._get_sensor", return_value=sensor), patch(
        "pygios.Gios._get_indexes", return_value=indexes
    ):
        async with ClientSession() as websession:
            gios = pygios.Gios(TEST_STATION_ID, websession)
            await gios.update()

        assert gios.station_name == TEST_STATION_NAME
        assert gios.latitude == TEST_LATITUDE
        assert gios.longitude == TEST_LONGITUDE
        assert gios.available == False
        assert gios.data == {}


@pytest.mark.asyncio
async def test_invalid_sensor_data():
    """Test with valid data."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with open("tests/data/station.json") as file:
        station = json.load(file)

    sensor = {}

    with open("tests/data/indexes.json") as file:
        indexes = json.load(file)

    with patch("pygios.Gios._get_stations", return_value=stations), patch(
        "pygios.Gios._get_station", return_value=station
    ), patch("pygios.Gios._get_sensor", return_value=sensor), patch(
        "pygios.Gios._get_indexes", return_value=indexes
    ):
        async with ClientSession() as websession:
            gios = pygios.Gios(TEST_STATION_ID, websession)
            await gios.update()

        assert gios.station_name == TEST_STATION_NAME
        assert gios.latitude == TEST_LATITUDE
        assert gios.longitude == TEST_LONGITUDE
        assert gios.available == False
        assert gios.data == {}


@pytest.mark.asyncio
async def test_invalid_station_data():
    """Test with valid data."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    station = {}

    with open("tests/data/sensor.json") as file:
        sensor = json.load(file)

    with open("tests/data/indexes.json") as file:
        indexes = json.load(file)

    with patch("pygios.Gios._get_stations", return_value=stations), patch(
        "pygios.Gios._get_station", return_value=station
    ), patch("pygios.Gios._get_sensor", return_value=sensor), patch(
        "pygios.Gios._get_indexes", return_value=indexes
    ):
        async with ClientSession() as websession:
            gios = pygios.Gios(TEST_STATION_ID, websession)
            await gios.update()

        assert gios.available == False
        assert gios.data == {}


@pytest.mark.asyncio
async def test_invalid_stations_data():
    """Test with valid data."""
    stations = {}

    with open("tests/data/station.json") as file:
        station = json.load(file)

    with open("tests/data/sensor.json") as file:
        sensor = json.load(file)

    with open("tests/data/indexes.json") as file:
        indexes = json.load(file)

    with patch("pygios.Gios._get_stations", return_value=stations), patch(
        "pygios.Gios._get_station", return_value=station
    ), patch("pygios.Gios._get_sensor", return_value=sensor), patch(
        "pygios.Gios._get_indexes", return_value=indexes
    ):
        async with ClientSession() as websession:
            gios = pygios.Gios(TEST_STATION_ID, websession)
            await gios.update()

        assert gios.available == False
        assert gios.data == {}

@pytest.mark.asyncio
async def test_invalid_station_id():
    """Test with valid data."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with open("tests/data/station.json") as file:
        station = json.load(file)

    with open("tests/data/sensor.json") as file:
        sensor = json.load(file)

    with open("tests/data/indexes.json") as file:
        indexes = json.load(file)

    with patch("pygios.Gios._get_stations", return_value=stations), patch(
        "pygios.Gios._get_station", return_value=station
    ), patch("pygios.Gios._get_sensor", return_value=sensor), patch(
        "pygios.Gios._get_indexes", return_value=indexes
    ), pytest.raises(pygios.NoStationError) as exception:

        async with ClientSession() as websession:
            gios = pygios.Gios(INVALID_STATION_ID, websession)
            await gios.update()

        assert exception.value == NO_MEASURING_STATION