"""
Python wrapper for getting air quality data from GIOS.
"""
import logging
from contextlib import suppress
from typing import Any, Dict, List, Optional, cast

from aiohttp import ClientSession
from dacite import from_dict

from .const import (
    ATTR_AQI,
    ATTR_ID,
    ATTR_INDEX,
    ATTR_INDEX_LEVEL,
    ATTR_NAME,
    ATTR_VALUE,
    HTTP_OK,
    URL_INDEXES,
    URL_SENSOR,
    URL_STATION,
    URL_STATIONS,
)
from .model import GiosSensors

_LOGGER = logging.getLogger(__name__)


class Gios:  # pylint:disable=(too-few-public-methods
    """Main class to perform GIOS API requests"""

    def __init__(self, station_id: int, session: ClientSession) -> None:
        """Initialize."""
        self.station_id = station_id
        self.latitude: Optional[float] = None
        self.longitude: Optional[float] = None
        self.station_name: Optional[str] = None
        self._station_data: List[Dict[str, Any]] = []

        self.session = session

    async def async_update(self) -> GiosSensors:  # pylint:disable=too-many-branches
        """Update GIOS data."""
        data: Dict[str, Dict[str, Any]] = {}
        invalid_sensors: List[str] = []

        if not self.station_name:
            stations = await self._get_stations()
            if not stations:
                raise ApiError("Invalid measuring stations list from GIOS API")

            for station in stations:
                if station[ATTR_ID] == self.station_id:
                    self.latitude = float(station["gegrLat"])
                    self.longitude = float(station["gegrLon"])
                    self.station_name = station["stationName"]
            if not self.station_name:
                raise NoStationError(
                    f"{self.station_id} is not a valid measuring station ID"
                )

            self._station_data = await self._get_station()

        if not self._station_data:
            raise InvalidSensorsData("Invalid measuring station data from GIOS API")

        for sensor_dict in self._station_data:
            data[sensor_dict["param"]["paramCode"].lower()] = {
                ATTR_ID: sensor_dict[ATTR_ID],
                ATTR_NAME: sensor_dict["param"]["paramName"],
            }

        sensors = await self._get_all_sensors(data)

        # The GIOS server sends a null values for sensors several minutes before
        # adding new data from measuring station. If the newest value is null
        # we take the earlier value.
        for sensor, sensor_data in data.items():
            try:
                if sensors[sensor]["values"][0][ATTR_VALUE]:
                    sensor_data[ATTR_VALUE] = sensors[sensor]["values"][0][ATTR_VALUE]
                elif sensors[sensor].get("values")[1][ATTR_VALUE]:
                    sensor_data[ATTR_VALUE] = sensors[sensor]["values"][1][ATTR_VALUE]
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

        for sensor, sensor_data in data.items():
            with suppress(IndexError, KeyError, TypeError):
                index_level = ATTR_INDEX_LEVEL.format(sensor.lower().replace(".", ""))
                sensor_data[ATTR_INDEX] = indexes[index_level]["indexLevelName"].lower()

        with suppress(IndexError, KeyError, TypeError):
            if indexes["stIndexLevel"]["indexLevelName"]:
                data[ATTR_AQI.lower()] = {ATTR_NAME: ATTR_AQI}
                data[ATTR_AQI.lower()][ATTR_VALUE] = indexes["stIndexLevel"][
                    "indexLevelName"
                ].lower()

        if data.get("pm2.5"):
            data["pm25"] = data.pop("pm2.5")

        return from_dict(data_class=GiosSensors, data=data)

    async def _get_stations(self) -> List[Dict[str, Any]]:
        """Retreive list of measuring stations."""
        return cast(List[Dict[str, Any]], await self._async_get(URL_STATIONS))

    async def _get_station(self) -> List[Dict[str, Any]]:
        """Retreive measuring station data."""
        url = URL_STATION.format(self.station_id)
        return cast(List[Dict[str, Any]], await self._async_get(url))

    async def _get_all_sensors(self, sensors: Dict[str, Any]) -> Dict[str, Any]:
        """Retreive all sensors data."""
        data: Dict[str, Any] = {}
        for sensor in sensors:
            sensor_data = await self._get_sensor(sensors[sensor][ATTR_ID])
            data[sensor] = sensor_data
        return data

    async def _get_sensor(self, sensor: int) -> Dict[str, Any]:
        """Retreive sensor data."""
        url = URL_SENSOR.format(sensor)
        return await self._async_get(url)

    async def _get_indexes(self) -> Dict[str, Any]:
        """Retreive indexes data."""
        url = URL_INDEXES.format(self.station_id)
        return await self._async_get(url)

    async def _async_get(self, url: str) -> Dict[str, Any]:
        """Retreive data from GIOS API."""
        data: Dict[str, Any] = {}
        async with self.session.get(url) as resp:
            _LOGGER.debug("Data retrieved from %s, status: %s", url, resp.status)
            if resp.status != HTTP_OK:
                _LOGGER.warning("Invalid response from GIOS API: %s", resp.status)
                raise ApiError(str(resp.status))
            data = await resp.json()
        return data


class ApiError(Exception):
    """Raised when GIOS API request ended in error."""

    def __init__(self, status: str) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status


class InvalidSensorsData(Exception):
    """Raised when sensors data is invalid."""

    def __init__(self, status: str) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status


class NoStationError(Exception):
    """Raised when no measuring station error."""

    def __init__(self, status: str) -> None:
        """Initialize."""
        super().__init__(status)
        self.status = status
