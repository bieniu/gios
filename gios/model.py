"""Type definitions for GIOS."""
from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class Sensor:
    """Data class for sensor."""

    name: str
    id: Optional[int]  # pylint: disable=invalid-name
    index: Optional[str] = None
    value: Optional[Union[float, str]] = None


@dataclass
class GiosSensors:  # pylint: disable=too-many-instance-attributes
    """Data class for polutants."""

    aqi: Optional[Sensor]
    c6h6: Optional[Sensor]
    co: Optional[Sensor]  # pylint: disable=invalid-name
    no2: Optional[Sensor]
    o3: Optional[Sensor]  # pylint: disable=invalid-name
    pm10: Optional[Sensor]
    pm25: Optional[Sensor]
    so2: Optional[Sensor]
