from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DriverGeoData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    driver_id: int
    latitude: float
    longitude: float
    altitude: float
    speed: float
    created_at: datetime = datetime.now()
