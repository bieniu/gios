"""Constants for GIOS library."""
ATTR_AQI: str = "AQI"
ATTR_ID: str = "id"
ATTR_INDEX: str = "index"
ATTR_INDEX_LEVEL: str = "{}IndexLevel"
ATTR_NAME: str = "name"
ATTR_VALUE: str = "value"

HTTP_OK: int = 200
URL_INDEXES: str = "http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{}"
URL_SENSOR: str = "http://api.gios.gov.pl/pjp-api/rest/data/getData/{}"
URL_STATION: str = "http://api.gios.gov.pl/pjp-api/rest/station/sensors/{}"
URL_STATIONS: str = "http://api.gios.gov.pl/pjp-api/rest/station/findAll"
