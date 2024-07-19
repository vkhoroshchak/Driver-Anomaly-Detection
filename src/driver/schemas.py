from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DriverGeoData(BaseModel):
    driver_id: int
    latitude: float
    longitude: float
    altitude: float
    speed: float
    created_at: datetime = datetime.now()

    class Config:
        model_config = ConfigDict(from_attributes=True)
        json_schema_extra = {
            "example": {
                "driver_id": 1,
                "latitude": 40.712776,
                "longitude": -74.005974,
                "altitude": 500.0,
                "speed": 60.0,
                "created_at": "2022-02-24T03:40:00",
            }
        }


class DriverGeoDataModelSchema(DriverGeoData):
    is_correct: bool

    class Config:
        json_schema_extra = {
            "example": {
                "driver_id": 1,
                "latitude": 40.712776,
                "longitude": -74.005974,
                "altitude": 500.0,
                "speed": 60.0,
                "created_at": "2022-02-24T03:40:00",
                "is_correct": True,
            }
        }
