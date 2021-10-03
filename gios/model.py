"""Type definitions for GIOS."""
from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class Sensor:
    """Data class for sensor."""

    name: str
    id: Optional[int]
    index: Optional[str] = None
    value: Optional[Union[float, str]] = None


@dataclass
class GiosSensors:
    """Data class for polutants."""

    aqi: Optional[Sensor]
    c6h6: Optional[Sensor]
    co: Optional[Sensor]
    no2: Optional[Sensor]
    o3: Optional[Sensor]
    pm10: Optional[Sensor]
    pm25: Optional[Sensor]
    so2: Optional[Sensor]
