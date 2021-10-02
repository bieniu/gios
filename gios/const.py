"""Constants for GIOS library."""
from typing import Final

ATTR_AQI: Final[str] = "AQI"
ATTR_ID: Final[str] = "id"
ATTR_INDEX: Final[str] = "index"
ATTR_INDEX_LEVEL: Final[str] = "{}IndexLevel"
ATTR_NAME: Final[str] = "name"
ATTR_VALUE: Final[str] = "value"

URL_INDEXES: Final[str] = "http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{}"
URL_SENSOR: Final[str] = "http://api.gios.gov.pl/pjp-api/rest/data/getData/{}"
URL_STATION: Final[str] = "http://api.gios.gov.pl/pjp-api/rest/station/sensors/{}"
URL_STATIONS: Final[str] = "http://api.gios.gov.pl/pjp-api/rest/station/findAll"
