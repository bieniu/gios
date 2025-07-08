"""Constants for GIOS library."""

from typing import Final

from yarl import URL

ATTR_AQI: Final[str] = "AQI"
ATTR_ID: Final[str] = "id"
ATTR_INDEX: Final[str] = "index"
ATTR_INDEX_LEVEL: Final[str] = "Nazwa kategorii indeksu dla wskażnika {}"
ATTR_NAME: Final[str] = "name"
ATTR_VALUE: Final[str] = "value"

URL_API_BASE: Final[URL] = URL("https://api.gios.gov.pl/pjp-api/v1/rest")

URL_INDEXES: Final[URL] = URL_API_BASE / "aqindex" / "getIndex"
URL_SENSOR: Final[URL] = URL_API_BASE / "data" / "getData"
URL_STATION: Final[URL] = URL_API_BASE / "station" / "sensors"
URL_STATIONS: Final[URL] = URL_API_BASE / "station" / "findAll"


POLLUTANT_MAP = {
    "benzen": "benzene",
    "dwutlenek azotu": "nitrogen dioxide",
    "dwutlenek siarki": "sulfur dioxide",
    "ozon": "ozone",
    "pył zawieszony PM10": "particulate matter 10",
    "pył zawieszony PM2.5": "particulate matter 2.5",
    "tlenek azotu": "nitrogen monoxide",
    "tlenek węgla": "carbon monoxide",
    "tlenki azotu": "nitrogen oxides",
}
STATE_MAP = {
    "Bardzo dobry": "very_good",
    "Bardzo zły": "very_bad",
    "Dobry": "good",
    "Dostateczny": "sufficient",
    "Umiarkowany": "moderate",
    "Zły": "bad",
}
