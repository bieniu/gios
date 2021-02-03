"""Tests for gios package."""
import json
from unittest.mock import patch

import pytest
from aiohttp import ClientSession

from gios import ApiError, Gios, InvalidSensorsData, NoStationError

INVALID_STATION_ID = 0

VALID_STATION_ID = 552
VALID_STATION_NAME = "Test Name"
VALID_LATITUDE = "99.99"
VALID_LONGITUDE = "88.88"


@pytest.mark.asyncio
async def test_valid_data_first_value():
    """Test with valid data and valid first sensor's value."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with open("tests/data/station.json") as file:
        station = json.load(file)

    with open("tests/data/sensors_valid_first_values.json") as file:
        sensors = json.load(file)

    with open("tests/data/indexes.json") as file:
        indexes = json.load(file)

    with patch("gios.Gios._get_stations", return_value=stations), patch(
        "gios.Gios._get_station", return_value=station
    ), patch("gios.Gios._get_all_sensors", return_value=sensors), patch(
        "gios.Gios._get_indexes", return_value=indexes
    ):

        async with ClientSession() as websession:
            gios = Gios(VALID_STATION_ID, websession)
            await gios.update()

        assert gios.station_name == VALID_STATION_NAME
        assert gios.station_id == VALID_STATION_ID
        assert gios.latitude == VALID_LATITUDE
        assert gios.longitude == VALID_LONGITUDE
        assert len(gios.data) == 8
        assert gios.available is True
        assert gios.data["SO2"]["value"] == 4.35478
        assert gios.data["SO2"]["index"] == "very good"
        assert gios.data["C6H6"]["value"] == 0.23789
        assert gios.data["C6H6"]["index"] == "very good"
        assert gios.data["CO"]["value"] == 251.874
        assert gios.data["CO"]["index"] == "very good"
        assert gios.data["NO2"]["value"] == 7.13411
        assert gios.data["NO2"]["index"] == "very good"
        assert gios.data["O3"]["value"] == 95.7768
        assert gios.data["O3"]["index"] == "good"
        assert gios.data["PM2.5"]["value"] == 4.11795
        assert gios.data["PM2.5"]["index"] == "very good"
        assert gios.data["PM10"]["value"] == 16.8344
        assert gios.data["PM10"]["index"] == "very good"
        assert gios.data["AQI"]["value"] == "good"


@pytest.mark.asyncio
async def test_valid_data_second_value():
    """Test with valid data and valid second sensor's value."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with open("tests/data/station.json") as file:
        station = json.load(file)

    with open("tests/data/sensors_valid_second_values.json") as file:
        sensors = json.load(file)

    with open("tests/data/indexes.json") as file:
        indexes = json.load(file)

    with patch("gios.Gios._get_stations", return_value=stations), patch(
        "gios.Gios._get_station", return_value=station
    ), patch("gios.Gios._get_all_sensors", return_value=sensors), patch(
        "gios.Gios._get_indexes", return_value=indexes
    ):

        async with ClientSession() as websession:
            gios = Gios(VALID_STATION_ID, websession)
            await gios.update()

        assert gios.station_name == VALID_STATION_NAME
        assert gios.station_id == VALID_STATION_ID
        assert gios.latitude == VALID_LATITUDE
        assert gios.longitude == VALID_LONGITUDE
        assert len(gios.data) == 8
        assert gios.available is True
        assert gios.data["SO2"]["value"] == 4.25478
        assert gios.data["SO2"]["index"] == "very good"
        assert gios.data["C6H6"]["value"] == 0.22789
        assert gios.data["C6H6"]["index"] == "very good"
        assert gios.data["CO"]["value"] == 250.874
        assert gios.data["CO"]["index"] == "very good"
        assert gios.data["NO2"]["value"] == 7.33411
        assert gios.data["NO2"]["index"] == "very good"
        assert gios.data["O3"]["value"] == 93.7768
        assert gios.data["O3"]["index"] == "good"
        assert gios.data["PM2.5"]["value"] == 4.21464
        assert gios.data["PM2.5"]["index"] == "very good"
        assert gios.data["PM10"]["value"] == 17.8344
        assert gios.data["PM10"]["index"] == "very good"
        assert gios.data["AQI"]["value"] == "good"


@pytest.mark.asyncio
async def test_no_indexes_data():
    """Test with valid data."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with open("tests/data/station.json") as file:
        station = json.load(file)

    with open("tests/data/sensors_valid_first_values.json") as file:
        sensors = json.load(file)

    indexes = {}

    with patch("gios.Gios._get_stations", return_value=stations), patch(
        "gios.Gios._get_station", return_value=station
    ), patch("gios.Gios._get_all_sensors", return_value=sensors), patch(
        "gios.Gios._get_indexes", return_value=indexes
    ), pytest.raises(
        InvalidSensorsData
    ) as error:

        async with ClientSession() as websession:
            gios = Gios(VALID_STATION_ID, websession)
            await gios.update()

    assert str(error.value) == "Invalid index data from GIOS API"
    assert gios.available is False


@pytest.mark.asyncio
async def test_no_sensor_data():
    """Test with no sensor data."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with open("tests/data/station.json") as file:
        station = json.load(file)

    sensors = {}

    with patch("gios.Gios._get_stations", return_value=stations), patch(
        "gios.Gios._get_station", return_value=station
    ), patch("gios.Gios._get_all_sensors", return_value=sensors), pytest.raises(
        InvalidSensorsData
    ) as error:

        async with ClientSession() as websession:
            gios = Gios(VALID_STATION_ID, websession)
            await gios.update()

    assert str(error.value) == "Invalid sensor data from GIOS API"
    assert gios.available is False


@pytest.mark.asyncio
async def test_invalid_sensor_data_1():
    """Test with invalid sensor data."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with open("tests/data/station.json") as file:
        station = json.load(file)

    with open("tests/data/sensors_invalid_1.json") as file:
        sensors = json.load(file)

    with patch("gios.Gios._get_stations", return_value=stations), patch(
        "gios.Gios._get_station", return_value=station
    ), patch("gios.Gios._get_all_sensors", return_value=sensors), pytest.raises(
        InvalidSensorsData
    ) as error:

        async with ClientSession() as websession:
            gios = Gios(VALID_STATION_ID, websession)
            await gios.update()

    assert str(error.value) == "Invalid sensor data from GIOS API"
    assert gios.available is False


@pytest.mark.asyncio
async def test_invalid_sensor_data_2():
    """Test with invalid sensor data."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with open("tests/data/station.json") as file:
        station = json.load(file)

    with open("tests/data/sensors_invalid_2.json") as file:
        sensors = json.load(file)

    with patch("gios.Gios._get_stations", return_value=stations), patch(
        "gios.Gios._get_station", return_value=station
    ), patch("gios.Gios._get_all_sensors", return_value=sensors), pytest.raises(
        InvalidSensorsData
    ) as error:

        async with ClientSession() as websession:
            gios = Gios(VALID_STATION_ID, websession)
            await gios.update()

    assert str(error.value) == "Invalid sensor data from GIOS API"
    assert gios.available is False


@pytest.mark.asyncio
async def test_invalid_sensor_data_3():
    """Test with invalid sensor data."""
    with open("tests/data/stations.json") as file:
        stations = json.load(file)

    with open("tests/data/station.json") as file:
        station = json.load(file)

    with open("tests/data/sensors_invalid_3.json") as file:
        sensors = json.load(file)

    with patch("gios.Gios._get_stations", return_value=stations), patch(
        "gios.Gios._get_station", return_value=station
    ), patch("gios.Gios._get_all_sensors", return_value=sensors), pytest.raises(
        InvalidSensorsData
    ) as error:

        async with ClientSession() as websession:
            gios = Gios(VALID_STATION_ID, websession)
            await gios.update()

    assert str(error.value) == "Invalid sensor data from GIOS API"
    assert gios.available is False


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
    assert gios.available is False


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
    assert gios.available is False


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
    assert gios.available is False
