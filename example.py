"""Example for GIOS."""

import asyncio
import logging

from aiohttp import ClientError, ClientSession

from gios import ApiError, Gios, InvalidSensorsDataError, NoStationError

GIOS_STATION_ID = 568

logging.basicConfig(level=logging.DEBUG)


async def main() -> None:
    """Run main function."""
    async with ClientSession() as websession:
        gios = Gios(GIOS_STATION_ID, websession)
        try:
            data = await gios.async_update()
        except (
            ApiError,
            NoStationError,
            InvalidSensorsDataError,
            ClientError,
        ) as error:
            print(error)
            return

    print(f"Measurement stations: {gios.measurement_stations}")
    print(f"Station: {gios.station_name} ({gios.latitude}, {gios.longitude})")
    print(data)


loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()
