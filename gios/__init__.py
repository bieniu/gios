"""Python wrapper for getting air quality data from GIOS."""

import asyncio
import logging
from collections.abc import Generator
from http import HTTPStatus
from typing import Any, Final, Self, cast

from aiohttp import ClientSession
from dacite import from_dict
from yarl import URL

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

        data = {
            sensor["Wskaźnik - wzór"].lower(): {
                ATTR_ID: sensor["Identyfikator stanowiska"],
                ATTR_NAME: POLLUTANT_MAP[sensor["Wskaźnik"]],
            }
            for sensor in self._station_data
            if sensor["Wskaźnik"] in POLLUTANT_MAP
        }

        sensors = await self._get_all_sensors(data)

        # The GIOS server sends null values for sensors several minutes before
        # adding new data from measuring station. If the newest value is null
        # we take the earlier value.
        for sensor, sensor_data in data.items():
            try:
                sensor_entry = sensors[sensor]["Lista danych pomiarowych"]
                if (
                    sensor_value := sensor_entry[0]["Wartość"]
                    or sensor_entry[1]["Wartość"]
                ):
                    sensor_data[ATTR_VALUE] = sensor_value
                else:
                    invalid_sensors.append(sensor)
            except (IndexError, KeyError, TypeError):
                invalid_sensors.append(sensor)

        for sensor in invalid_sensors:
            data.pop(sensor)

        if not data:
            msg = "Invalid sensor data from GIOS API"
            raise InvalidSensorsDataError(msg)

        indexes = await self._get_indexes()

        for sensor, sensor_data in data.items():
            if index_value := indexes.get("AqIndex", {}).get(
                ATTR_INDEX_LEVEL.format(sensor.upper())
            ):
                sensor_data[ATTR_INDEX] = STATE_MAP[index_value]

        if (aq_index := indexes.get("AqIndex", {})).get(
            "Status indeksu ogólnego dla stacji pomiarowej"
        ) and (index_value := aq_index.get("Nazwa kategorii indeksu")):
            data[ATTR_AQI.lower()] = {
                ATTR_NAME: ATTR_AQI,
                ATTR_VALUE: STATE_MAP[index_value],
            }

        if data.get("pm2.5"):
            data["pm25"] = data.pop("pm2.5")

        result: GiosSensors = from_dict(data_class=GiosSensors, data=data)
        return result

    async def _get_stations(self) -> Any:
        """Retrieve list of measurement stations."""
        result = await self._async_get(URL_STATIONS.with_query(page=0, size=1000))
        return result.get("Lista stacji pomiarowych", [])

    def _parse_stations(self, stations: list[dict[str, Any]]) -> Generator[GiosStation]:
        """Parse stations data."""
        for station in stations:
            yield GiosStation(
                cast(int, station["Identyfikator stacji"]),
                station["Nazwa stacji"],
                float(station["WGS84 φ N"]),
                float(station["WGS84 λ E"]),
            )

    async def _get_station(self) -> Any:
        """Retrieve measuring station data."""
        url = URL_STATION / str(self.station_id)
        result = await self._async_get(url)
        return result.get("Lista stanowisk pomiarowych dla podanej stacji", [])

    async def _get_all_sensors(self, sensors: dict[str, Any]) -> dict[str, Any]:
        """Retrieve all sensors data."""
        tasks = [self._get_sensor(sensors[sensor][ATTR_ID]) for sensor in sensors]
        results = await asyncio.gather(*tasks)
        return dict(zip(sensors, results, strict=True))

    async def _get_sensor(self, sensor: int) -> Any:
        """Retrieve sensor data."""
        url = URL_SENSOR / str(sensor)
        return await self._async_get(url, do_not_raise=True)

    async def _get_indexes(self) -> Any:
        """Retrieve indexes data."""
        url = URL_INDEXES / str(self.station_id)
        return await self._async_get(url)

    async def _async_get(self, url: URL, do_not_raise: bool = False) -> Any:
        """Retrieve data from GIOS API."""
        async with self.session.get(url) as resp:
            _LOGGER.debug("Data retrieved from %s, status: %s", url, resp.status)
            if resp.status != HTTPStatus.OK.value:
                msg = f"Invalid response from GIOS API: {resp.status}"

                if do_not_raise:
                    _LOGGER.info(msg)
                    return {}

                _LOGGER.warning(msg)
                raise ApiError(str(resp.status))

            return await resp.json()
