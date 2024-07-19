from abc import ABC, abstractmethod

from geopy import distance
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db import Base
from driver.models import DriverGeoData
from driver.schemas import DriverGeoData as DriverGeoDataSchema
from utils.logger import BaseLogger

logger = BaseLogger().get_logger(__name__)


class DatabaseInterface(ABC):
    @abstractmethod
    async def get_latest_data(self, *args, **kwargs) -> Base:
        pass

    @abstractmethod
    async def insert_data(self, data: Base, *args, **kwargs) -> Base:
        pass


class DriverGeoDataDB(DatabaseInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_latest_data(self, data: DriverGeoDataSchema, *args, **kwargs) -> DriverGeoData:
        query = await self.session.execute(
            select(DriverGeoData)
            .filter(DriverGeoData.driver_id == data.driver_id)
            .order_by(DriverGeoData.created_at.desc())
        )
        res = query.scalars().first()
        return res

    async def insert_data(self, data: DriverGeoData, *args, **kwargs) -> DriverGeoData:
        self.session.add(data)
        await self.session.commit()
        return data


def is_anomalous(data: DriverGeoDataSchema, previous_data: DriverGeoDataSchema | None) -> bool:
    # Check if speed or altitude is out of bounds
    if data.speed > settings.THRESHOLDS.MAX_SPEED_KMH:
        return True
    if data.altitude < 0 or data.altitude > settings.THRESHOLDS.MAX_ALTITUDE_M:
        return True

    if previous_data:
        distance_km = distance.distance(
            (previous_data.latitude, previous_data.longitude), (data.latitude, data.longitude)
        ).km

        logger.debug(f"Distance: {distance_km}")
        # time diff in hours
        time_diff = (data.created_at - previous_data.created_at).total_seconds() / 3600
        logger.debug(f"Time diff: {time_diff}")

        try:
            required_speed = distance_km / time_diff
        except ZeroDivisionError:
            if distance_km > 0:
                return True
        else:
            logger.debug(f"Required speed: {required_speed}")
            if required_speed > data.speed:
                return True
    return False
