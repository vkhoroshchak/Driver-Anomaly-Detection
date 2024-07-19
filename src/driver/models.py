from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


class DriverGeoData(Base):
    __tablename__ = "driver_geo_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    driver_id: Mapped[int]
    latitude: Mapped[float]
    longitude: Mapped[float]
    altitude: Mapped[float]
    speed: Mapped[float]
    is_correct: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now())
