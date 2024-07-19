import asyncio
import json
import random

import aiohttp

with open("settings.json") as f:
    settings = json.load(f)


# Generate random coordinates in the area of Lviv
def generate_random_coordinates() -> dict:
    lat_min, lat_max = 49.795, 49.915
    lon_min, lon_max = 23.916, 24.091
    return {
        "latitude": random.uniform(lat_min, lat_max),
        "longitude": random.uniform(lon_min, lon_max),
        "speed": random.uniform(0, settings["THRESHOLDS"]["MAX_SPEED_KMH"]),
        "altitude": random.uniform(0, settings["THRESHOLDS"]["MAX_ALTITUDE_M"]),
    }


async def send_driver_data(session: aiohttp.ClientSession, driver_id: int) -> None:
    while True:
        data = generate_random_coordinates()
        data["driver_id"] = driver_id
        async with session.post(settings["SERVER_URL"], json=data) as response:
            if response.status != 200:
                print(f"Failed to send data for driver {driver_id}: {await response.json()}")
        await asyncio.sleep(settings["INTERVAL_SECONDS"])


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        tasks = [send_driver_data(session, driver_id) for driver_id in range(1, settings["NUM_DRIVERS"] + 1)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
