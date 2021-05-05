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
            data = await gios.update()
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
