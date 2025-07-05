"""Type definitions for GIOS."""

from dataclasses import dataclass


@dataclass
class Sensor:
    """Data class for sensor."""

    name: str
    id: int | None
    index: str | None = None
    value: float | str | None = None


@dataclass
class GiosSensors:
    """Data class for polutants."""

    aqi: Sensor | None
    c6h6: Sensor | None
    co: Sensor | None
    no: Sensor | None
    no2: Sensor | None
    nox: Sensor | None
    o3: Sensor | None
    pm10: Sensor | None
    pm25: Sensor | None
    so2: Sensor | None


@dataclass
class GiosStation:
    """Data class for measeurement station."""

    id: int
    name: str
    latitude: float
    longitude: float
