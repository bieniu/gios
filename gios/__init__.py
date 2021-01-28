"""
Python wrapper for getting air quality data from GIOS.
"""
import logging

_LOGGER = logging.getLogger(__name__)

ATTR_AQI = "AQI"
ATTR_ID = "id"
ATTR_INDEX = "index"
ATTR_INDEX_LEVEL = "{}IndexLevel"
ATTR_NAME = "name"
ATTR_VALUE = "value"

HTTP_OK = 200
URL_INDEXES = "http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{}"
URL_SENSOR = "http://api.gios.gov.pl/pjp-api/rest/data/getData/{}"
URL_STATION = "http://api.gios.gov.pl/pjp-api/rest/station/sensors/{}"
URL_STATIONS = "http://api.gios.gov.pl/pjp-api/rest/station/findAll"


class Gios:  # pylint:disable=too-many-instance-attributes
    """Main class to perform GIOS API requests"""

    def __init__(self, station_id, session):
        """Initialize."""
        self.data = {}
        self.station_id = station_id
        self.latitude = None
        self.longitude = None
        self.station_name = None
        self._station_data = {}
        self._available = False

        self.session = session

    async def update(self):  # pylint:disable=too-many-branches
        """Update GIOS data."""
        data = {}
        invalid_sensors = []

        if not self.station_name:
            stations = await self._get_stations()
            if not stations:
                self._available = False
                raise ApiError("Invalid measuring stations list from GIOS API")

            for station in stations:
                if station[ATTR_ID] == self.station_id:
                    self.latitude = station["gegrLat"]
                    self.longitude = station["gegrLon"]
                    self.station_name = station["stationName"]
            if not self.station_name:
                self._available = False
                raise NoStationError(
                    f"{self.station_id} is not a valid measuring station ID"
                )

            self._station_data = await self._get_station()

        if not self._station_data:
            self._available = False
            raise InvalidSensorsData("Invalid measuring station data from GIOS API")

        for sensor in self._station_data:
            data[sensor["param"]["paramCode"]] = {
                ATTR_ID: sensor[ATTR_ID],
                ATTR_NAME: sensor["param"]["paramName"],
            }

        sensors = await self._get_all_sensors(data)

        # The GIOS server sends a null values for sensors several minutes before
        # adding new data from measuring station. If the newest value is null
        # we take the earlier value.
        for sensor in data:
            try:
                if sensors[sensor]["values"][0][ATTR_VALUE]:
                    data[sensor][ATTR_VALUE] = sensors[sensor]["values"][0][ATTR_VALUE]
                elif sensors[sensor].get("values")[1][ATTR_VALUE]:
                    data[sensor][ATTR_VALUE] = sensors[sensor]["values"][1][ATTR_VALUE]
                else:
                    invalid_sensors.append(sensor)
            except (IndexError, KeyError, TypeError):
                invalid_sensors.append(sensor)

        if invalid_sensors:
            for sensor in invalid_sensors:
                data.pop(sensor)

        if not data:
            raise InvalidSensorsData("Invalid sensor data from GIOS API")

        indexes = await self._get_indexes()

        try:
            for sensor in data:
                index_level = ATTR_INDEX_LEVEL.format(sensor.lower().replace(".", ""))
                data[sensor][ATTR_INDEX] = indexes[index_level][
                    "indexLevelName"
                ].lower()

            data[ATTR_AQI] = {ATTR_NAME: ATTR_AQI}
            data[ATTR_AQI][ATTR_VALUE] = indexes["stIndexLevel"][
                "indexLevelName"
            ].lower()
        except (IndexError, KeyError, TypeError) as err:
            self._available = False
            raise InvalidSensorsData("Invalid index data from GIOS API") from err
        self._available = True
        self.data = data

    async def _get_stations(self):
        """Retreive list of measuring stations."""
        stations = await self._async_get(URL_STATIONS)
        return stations

    async def _get_station(self):
        """Retreive measuring station data."""
        url = URL_STATION.format(self.station_id)
        station = await self._async_get(url)
        return station

    async def _get_all_sensors(self, sensors):
        """Retreive all sensors data."""
        data = {}
        for sensor in sensors:
            sensor_data = await self._get_sensor(sensors[sensor][ATTR_ID])
            data[sensor] = sensor_data
        return data

    async def _get_sensor(self, sensor):
        """Retreive sensor data."""
        url = URL_SENSOR.format(sensor)
        sensor = await self._async_get(url)
        return sensor

    async def _get_indexes(self):
        """Retreive indexes data."""
        url = URL_INDEXES.format(self.station_id)
        indexes = await self._async_get(url)
        return indexes

    async def _async_get(self, url):
        """Retreive data from GIOS API."""
        data = None
        async with self.session.get(url) as resp:
            if resp.status != HTTP_OK:
                _LOGGER.warning("Invalid response from GIOS API: %s", resp.status)
                self._available = False
                raise ApiError(resp.status)
            data = await resp.json()
        _LOGGER.debug("Data retrieved from %s, status: %s", url, resp.status)
        return data

    @property
    def available(self):
        """Return True is data is available."""
        return bool(self.data)


class ApiError(Exception):
    """Raised when GIOS API request ended in error."""

    def __init__(self, status):
        """Initialize."""
        super().__init__(status)
        self.status = status


class InvalidSensorsData(Exception):
    """Raised when sensors data is invalid."""

    def __init__(self, status):
        """Initialize."""
        super().__init__(status)
        self.status = status


class NoStationError(Exception):
    """Raised when no measuring station error."""

    def __init__(self, status):
        """Initialize."""
        super().__init__(status)
        self.status = status
