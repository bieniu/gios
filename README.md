[![GitHub Release][releases-shield]][releases]
[![PyPI][pypi-releases-shield]][pypi-releases]
[![PyPI - Downloads][pypi-downloads]][pypi-statistics]
[![Buy me a coffee][buy-me-a-coffee-shield]][buy-me-a-coffee]
[![PayPal_Me][paypal-me-shield]][paypal-me]

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
import logging

from aiohttp import ClientError, ClientSession
from gios import ApiError, InvalidSensorsData, Gios, NoStationError

GIOS_STATION_ID = 117

logging.basicConfig(level=logging.DEBUG)

async def main():
    try:
        async with ClientSession() as websession:
            gios = Gios(GIOS_STATION_ID, websession)
            data = await gios.async_update()
    except (ApiError, NoStationError, InvalidSensorsData, ClientError) as error:
        print(f"{error}")
        return

    latitude = gios.latitude
    longitude = gios.longitude
    station_name = gios.station_name
    print(f"Longitude: {longitude}")
    print(f"Latitude: {latitude}")
    print(f"Station name: {station_name}")
    print(data)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

```
[releases]: https://github.com/bieniu/gios/releases
[releases-shield]: https://img.shields.io/github/release/bieniu/gios.svg?style=popout
[pypi-releases]: https://pypi.org/project/gios/
[pypi-statistics]: https://pepy.tech/project/gios
[pypi-releases-shield]: https://img.shields.io/pypi/v/gios
[pypi-downloads]: https://pepy.tech/badge/gios/month
[buy-me-a-coffee-shield]: https://img.shields.io/static/v1.svg?label=%20&message=Buy%20me%20a%20coffee&color=6f4e37&logo=buy%20me%20a%20coffee&logoColor=white
[buy-me-a-coffee]: https://www.buymeacoffee.com/QnLdxeaqO
[paypal-me-shield]: https://img.shields.io/static/v1.svg?label=%20&message=PayPal.Me&logo=paypal
[paypal-me]: https://www.paypal.me/bieniu79
