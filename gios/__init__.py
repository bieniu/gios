"""Python wrapper for getting air quality data from GIOS."""

import asyncio
import logging
from collections.abc import Generator
from contextlib import suppress
from http import HTTPStatus
from typing import Any, Final, Self, cast

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
from .model import GiosSensors, GiosStation

_LOGGER: Final = logging.getLogger(__name__)


class Gios:
    """Main class to perform GIOS API requests."""

    def __init__(self, station_id: int | None, session: ClientSession) -> None:
        """Initialize."""
        self.station_id = station_id
        self.latitude: float | None = None
        self.longitude: float | None = None
        self.station_name: str | None = None
        self._station_data: list[dict[str, Any]] = []
        self._measurement_stations: dict[int, GiosStation] = {}

        self.session = session

    @classmethod
    async def create(
        cls: type[Self],
        session: ClientSession,
        station_id: int | None = None,
    ) -> Self:
        """Create a new instance."""
        instance = cls(station_id, session)

        await instance.initialize()

        return instance

    async def initialize(self) -> None:
        """Initialize."""
        msg = "Initializing GIOS"
        if self.station_id:
            msg += f" for station ID: {self.station_id}"
        _LOGGER.debug(msg)

        stations = await self._get_stations()
        self._measurement_stations = {
            station.id: station for station in self._parse_stations(stations)
        }

        if self.station_id is None:
            return

        if (station := self.measurement_stations.get(self.station_id)) is None:
            msg = f"{self.station_id} is not a valid measuring station ID"
            raise NoStationError(msg)

        self.latitude = station.latitude
        self.longitude = station.longitude
        self.station_name = station.name

    @property
    def measurement_stations(self) -> dict[int, GiosStation]:
        """Return measurement stations dict."""
        return self._measurement_stations

    async def async_update(self) -> GiosSensors:
        """Update GIOS data."""
        if self.station_id is None:
            msg = "Measuring station ID is not set"
            raise NoStationError(msg)

        data: dict[str, dict[str, Any]] = {}
        invalid_sensors: list[str] = []

        if not self._station_data:
            self._station_data = await self._get_station()

        if not self._station_data:
            msg = "Invalid measuring station data from GIOS API"
            raise InvalidSensorsDataError(msg)

        for sensor_dict in self._station_data:
            data[sensor_dict["param"]["paramCode"].lower()] = {
                ATTR_ID: sensor_dict[ATTR_ID],
                ATTR_NAME: POLLUTANT_MAP[sensor_dict["param"]["paramName"]],
            }

        sensors = await self._get_all_sensors(data)

        # The GIOS server sends null values for sensors several minutes before
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
            msg = "Invalid sensor data from GIOS API"
            raise InvalidSensorsDataError(msg)

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
        """Retrieve list of measurement stations."""
        return await self._async_get(URL_STATIONS)

    def _parse_stations(self, stations: list[dict[str, Any]]) -> Generator[GiosStation]:
        """Parse stations data."""
        for station in stations:
            yield GiosStation(
                cast(int, station["id"]),
                station["stationName"],
                float(station["gegrLat"]),
                float(station["gegrLon"]),
            )

    async def _get_station(self) -> Any:
        """Retrieve measuring station data."""
        url = URL_STATION.format(self.station_id)
        return await self._async_get(url)

    async def _get_all_sensors(self, sensors: dict[str, Any]) -> dict[str, Any]:
        """Retrieve all sensors data."""
        tasks = [self._get_sensor(sensors[sensor][ATTR_ID]) for sensor in sensors]
        results = await asyncio.gather(*tasks)
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
