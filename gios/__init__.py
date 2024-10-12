"""Python wrapper for getting air quality data from GIOS."""

import asyncio
import logging
from contextlib import suppress
from http import HTTPStatus
from typing import Any, Final

from aiohttp import ClientSession
from dacite import from_dict

from .const import (
    ATTR_AQI,
    ATTR_ID,
    ATTR_INDEX,
    ATTR_INDEX_LEVEL,
    ATTR_NAME,
    ATTR_VALUE,
    POLLUTANT_MAP,
    STATE_MAP,
    URL_INDEXES,
    URL_SENSOR,
    URL_STATION,
    URL_STATIONS,
)
from .exceptions import ApiError, InvalidSensorsDataError, NoStationError
from .model import GiosSensors

_LOGGER: Final = logging.getLogger(__name__)


class Gios:
    """Main class to perform GIOS API requests."""

    def __init__(self, station_id: int, session: ClientSession) -> None:
        """Initialize."""
        self.station_id = station_id
        self.latitude: float | None = None
        self.longitude: float | None = None
        self.station_name: str | None = None
        self._station_data: list[dict[str, Any]] = []

        self.session = session

        _LOGGER.info("Initializing GIOS for station ID: %s", self.station_id)

    async def async_update(self) -> GiosSensors:
        """Update GIOS data."""
        data: dict[str, dict[str, Any]] = {}
        invalid_sensors: list[str] = []

        if not self.station_name:
            if not (stations := await self._get_stations()):
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
            raise InvalidSensorsDataError(
                "Invalid measuring station data from GIOS API"
            )

        for sensor_dict in self._station_data:
            data[sensor_dict["param"]["paramCode"].lower()] = {
                ATTR_ID: sensor_dict[ATTR_ID],
                ATTR_NAME: POLLUTANT_MAP[sensor_dict["param"]["paramName"]],
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
            raise InvalidSensorsDataError("Invalid sensor data from GIOS API")

        indexes = await self._get_indexes()

        for sensor, sensor_data in data.items():
            with suppress(IndexError, KeyError, TypeError):
                index_level = ATTR_INDEX_LEVEL.format(sensor.lower().replace(".", ""))
                sensor_data[ATTR_INDEX] = STATE_MAP[
                    indexes[index_level]["indexLevelName"]
                ]

        with suppress(IndexError, KeyError, TypeError):
            if indexes["stIndexLevel"]["indexLevelName"]:
                data[ATTR_AQI.lower()] = {ATTR_NAME: ATTR_AQI}
                data[ATTR_AQI.lower()][ATTR_VALUE] = STATE_MAP[
                    indexes["stIndexLevel"]["indexLevelName"]
                ]

        if data.get("pm2.5"):
            data["pm25"] = data.pop("pm2.5")

        result: GiosSensors = from_dict(data_class=GiosSensors, data=data)
        return result

    async def _get_stations(self) -> Any:
        """Retrieve list of measuring stations."""
        return await self._async_get(URL_STATIONS)

    async def _get_station(self) -> Any:
        """Retrieve measuring station data."""
        url = URL_STATION.format(self.station_id)
        return await self._async_get(url)

    async def _get_all_sensors(self, sensors: dict[str, Any]) -> dict[str, Any]:
        """Retrieve all sensors data."""
        results = await asyncio.gather(
            *[self._get_sensor(sensors[sensor][ATTR_ID]) for sensor in sensors]
        )
        return dict(zip(sensors, results, strict=True))

    async def _get_sensor(self, sensor: int) -> Any:
        """Retrieve sensor data."""
        url = URL_SENSOR.format(sensor)
        return await self._async_get(url)

    async def _get_indexes(self) -> Any:
        """Retrieve indexes data."""
        url = URL_INDEXES.format(self.station_id)
        return await self._async_get(url)

    async def _async_get(self, url: str) -> Any:
        """Retrieve data from GIOS API."""
        async with self.session.get(url) as resp:
            _LOGGER.debug("Data retrieved from %s, status: %s", url, resp.status)
            if resp.status != HTTPStatus.OK.value:
                _LOGGER.warning("Invalid response from GIOS API: %s", resp.status)
                raise ApiError(str(resp.status))

            return await resp.json()
