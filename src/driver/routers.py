from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from driver.models import DriverGeoData as DriverGeoDataModel
from driver.schemas import DriverGeoData as DriverGeoDataSchema
from driver.services import DriverGeoDataDB, is_anomalous
from utils.logger import BaseLogger

driver_router = APIRouter()

logger = BaseLogger().get_logger(__name__)


@driver_router.post("/driver-geo", response_model=DriverGeoDataSchema)
async def receive_driver_geo_data(
    driver_geo_data: DriverGeoDataSchema, db: AsyncSession = Depends(get_async_session)
) -> DriverGeoDataSchema:
    driver_db = DriverGeoDataDB(session=db)

    logger.info(f"Received driver geo data: {driver_geo_data}")
    latest_driver_geo_data = await driver_db.get_latest_data(driver_geo_data)
    logger.info(f"Latest driver geo data: {latest_driver_geo_data}")

    logger.info("Checking if data is anomalous...")
    is_correct = not is_anomalous(driver_geo_data, latest_driver_geo_data)

    if not is_correct:
        logger.warning("Data is anomalous!")

    driver_db_data = DriverGeoDataModel(**driver_geo_data.dict(), is_correct=is_correct)
    new_data = await driver_db.insert_data(driver_db_data)
    return new_data
