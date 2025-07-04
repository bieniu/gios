"""Constants for GIOS library."""

from typing import Final

ATTR_AQI: Final[str] = "AQI"
ATTR_ID: Final[str] = "id"
ATTR_INDEX: Final[str] = "index"
ATTR_INDEX_LEVEL: Final[str] = "Nazwa kategorii indeksu dla wskażnika {}"
ATTR_NAME: Final[str] = "name"
ATTR_VALUE: Final[str] = "value"

URL_INDEXES: Final[str] = "https://api.gios.gov.pl/pjp-api/v1/rest/aqindex/getIndex/{}"
URL_SENSOR: Final[str] = "https://api.gios.gov.pl/pjp-api/v1/rest/data/getData/{}"
URL_STATION: Final[str] = "https://api.gios.gov.pl/pjp-api/v1/rest/station/sensors/{}"
URL_STATIONS: Final[str] = (
    "https://api.gios.gov.pl/pjp-api/v1/rest/station/findAll?page=0&size=1000"
)

POLLUTANT_MAP = {
    "benzen": "benzene",
    "dwutlenek azotu": "nitrogen dioxide",
    "dwutlenek siarki": "sulfur dioxide",
    "ozon": "ozone",
    "pył zawieszony PM10": "particulate matter 10",
    "pył zawieszony PM2.5": "particulate matter 2.5",
    "tlenek azotu": "nitrogen monoxide",
    "tlenek węgla": "carbon monoxide",
    "tleneki azotu": "nitrogen oxides",
}
STATE_MAP = {
    "Bardzo dobry": "very_good",
    "Bardzo zły": "very_bad",
    "Dobry": "good",
    "Dostateczny": "sufficient",
    "Umiarkowany": "moderate",
    "Zły": "bad",
}
