"""Tests for gios package."""
import json

from aiohttp import ClientSession
from asynctest import patch
from gios import ApiError, Gios, InvalidSensorsData, NoStationError
import pytest

INVALID_STATION_ID = 0

VALID_STATION_ID = 552
VALID_STATION_NAME = "Test Name"
VALID_LATITUDE = "99.99"
VALID_LONGITUDE = "88.88"
VALID_AQI_VALUE = "good"
VALID_PM10_FIRST_VALUE = 11.11
VALID_PM10_SECOND_VALUE = 12.12


@pytest.mark.asyncio
async def test_valid_data_first_value():
    """Test with valid data and valid first sensor's value."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with open("tests/data/station.json") as file:
        station = json.load(file)

    with open("tests/data/sensor_valid_first.json") as file:
        sensor = json.load(file)

    with open("tests/data/indexes.json") as file:
        indexes = json.load(file)

    with patch("gios.Gios._get_stations", return_value=stations), patch(
        "gios.Gios._get_station", return_value=station
    ), patch("gios.Gios._get_sensor", return_value=sensor), patch(
        "gios.Gios._get_indexes", return_value=indexes
    ):

        async with ClientSession() as websession:
            gios = Gios(VALID_STATION_ID, websession)
            await gios.update()

        assert gios.station_name == VALID_STATION_NAME
        assert gios.station_id == VALID_STATION_ID
        assert gios.latitude == VALID_LATITUDE
        assert gios.longitude == VALID_LONGITUDE
        assert len(gios.data) == 2
        assert gios.available == True
        assert gios.data["PM10"]["value"] == VALID_PM10_FIRST_VALUE
        assert gios.data["AQI"]["value"] == VALID_AQI_VALUE


@pytest.mark.asyncio
async def test_valid_data_second_value():
    """Test with valid data and valid second sensor's value."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with open("tests/data/station.json") as file:
        station = json.load(file)

    with open("tests/data/sensor_valid_second.json") as file:
        sensor = json.load(file)

    with open("tests/data/indexes.json") as file:
        indexes = json.load(file)

    with patch("gios.Gios._get_stations", return_value=stations), patch(
        "gios.Gios._get_station", return_value=station
    ), patch("gios.Gios._get_sensor", return_value=sensor), patch(
        "gios.Gios._get_indexes", return_value=indexes
    ):

        async with ClientSession() as websession:
            gios = Gios(VALID_STATION_ID, websession)
            await gios.update()

        assert gios.station_name == VALID_STATION_NAME
        assert gios.station_id == VALID_STATION_ID
        assert gios.latitude == VALID_LATITUDE
        assert gios.longitude == VALID_LONGITUDE
        assert len(gios.data) == 2
        assert gios.available == True
        assert gios.data["PM10"]["value"] == VALID_PM10_SECOND_VALUE
        assert gios.data["AQI"]["value"] == VALID_AQI_VALUE


@pytest.mark.asyncio
async def test_no_indexes_data():
    """Test with valid data."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with open("tests/data/station.json") as file:
        station = json.load(file)

    with open("tests/data/sensor_valid_first.json") as file:
        sensor = json.load(file)

    indexes = {}

    with patch("gios.Gios._get_stations", return_value=stations), patch(
        "gios.Gios._get_station", return_value=station
    ), patch("gios.Gios._get_sensor", return_value=sensor), patch(
        "gios.Gios._get_indexes", return_value=indexes
    ), pytest.raises(
        InvalidSensorsData
    ) as error:

        async with ClientSession() as websession:
            gios = Gios(VALID_STATION_ID, websession)
            await gios.update()

    assert str(error.value) == "Invalid index data from GIOS API"
    assert gios.available == False


@pytest.mark.asyncio
async def test_no_sensor_data():
    """Test with no sensor data."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with open("tests/data/station.json") as file:
        station = json.load(file)

    sensor = {}

    with patch("gios.Gios._get_stations", return_value=stations), patch(
        "gios.Gios._get_station", return_value=station
    ), patch("gios.Gios._get_sensor", return_value=sensor), pytest.raises(
        InvalidSensorsData
    ) as error:

        async with ClientSession() as websession:
            gios = Gios(VALID_STATION_ID, websession)
            await gios.update()

    assert str(error.value) == "Invalid sensor data from GIOS API"
    assert gios.available == False


@pytest.mark.asyncio
async def test_invalid_sensor_data_1():
    """Test with invalid sensor data."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with open("tests/data/station.json") as file:
        station = json.load(file)

    with open("tests/data/sensor_invalid_1.json") as file:
        sensor = json.load(file)

    with patch("gios.Gios._get_stations", return_value=stations), patch(
        "gios.Gios._get_station", return_value=station
    ), patch("gios.Gios._get_sensor", return_value=sensor), pytest.raises(
        InvalidSensorsData
    ) as error:

        async with ClientSession() as websession:
            gios = Gios(VALID_STATION_ID, websession)
            await gios.update()

    assert str(error.value) == "Invalid sensor data from GIOS API"
    assert gios.available == False


@pytest.mark.asyncio
async def test_invalid_sensor_data_2():
    """Test with invalid sensor data."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with open("tests/data/station.json") as file:
        station = json.load(file)

    with open("tests/data/sensor_invalid_2.json") as file:
        sensor = json.load(file)

    with patch("gios.Gios._get_stations", return_value=stations), patch(
        "gios.Gios._get_station", return_value=station
    ), patch("gios.Gios._get_sensor", return_value=sensor), pytest.raises(
        InvalidSensorsData
    ) as error:

        async with ClientSession() as websession:
            gios = Gios(VALID_STATION_ID, websession)
            await gios.update()

    assert str(error.value) == "Invalid sensor data from GIOS API"
    assert gios.available == False


@pytest.mark.asyncio
async def test_no_station_data():
    """Test with no station data."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    station = {}

    with patch("gios.Gios._get_stations", return_value=stations), patch(
        "gios.Gios._get_station", return_value=station
    ), pytest.raises(InvalidSensorsData) as error:
        async with ClientSession() as websession:
            gios = Gios(VALID_STATION_ID, websession)
            await gios.update()

    assert str(error.value) == "Invalid measuring station data from GIOS API"


@pytest.mark.asyncio
async def test_no_stations_data():
    """Test with no stations data."""
    stations = {}

    with patch("gios.Gios._async_get", return_value=stations), pytest.raises(
        ApiError
    ) as error:

        async with ClientSession() as websession:
            gios = Gios(VALID_STATION_ID, websession)
            await gios.update()

    assert str(error.value) == "Invalid measuring stations list from GIOS API"
    assert gios.available == False


@pytest.mark.asyncio
async def test_invalid_station_id():
    """Test with invalid station_id."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with patch("gios.Gios._get_stations", return_value=stations), pytest.raises(
        NoStationError
    ) as error:

        async with ClientSession() as websession:
            gios = Gios(INVALID_STATION_ID, websession)
            await gios.update()

    assert str(error.value) == "0 is not a valid measuring station ID"
    assert gios.available == False


@pytest.mark.asyncio
async def test_api_error():
    """Test GIOS API error."""
    with patch("gios.Gios._async_get", side_effect=ApiError(404)), pytest.raises(
        ApiError
    ) as error:

        async with ClientSession() as websession:
            gios = Gios(VALID_STATION_ID, websession)
            await gios.update()
    assert str(error.value) == "404"
    assert gios.available == False
