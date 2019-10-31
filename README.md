# gios
Python wrapper for getting air quality data from [GIOŚ (Główny Inspektorat Ochrony Środowiska)](http://www.gios.gov.pl/pl/stan-srodowiska/monitoring-jakosci-powietrza)

## How to find station_id
- go to http://powietrze.gios.gov.pl/pjp/current
- find on the map a measurement station located closest to your home
- go to "More info" link
- look at site address, for ex. for this address http://powietrze.gios.gov.pl/pjp/current/station_details/chart/291 `station_id` is 291

## How to use package
```python
import asyncio

from aiohttp import ClientSession
from gios import Gios, ApiError, NoStationError

GIOS_STATION_ID = 11794


async def main():
    try:
        async with ClientSession() as websession:
            gios = Gios(GIOS_STATION_ID, websession)
            await gios.update()
    except (ApiError, NoStationError) as error:
        print(f"{error}")
        return

    data = gios.data
    available = gios.available
    latitude = gios.latitude
    longitude = gios.longitude
    station_name = gios.station_name

    if available:
        print(f"Data available: {available}")
        print(
            f"Longitude: {longitude}, latitude: {latitude}, station name: {station_name}"
        )
        print(data)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

```
