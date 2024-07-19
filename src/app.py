import asyncio
import concurrent.futures
import time

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from core.config import settings
from core.db import get_async_session
from driver.routers import driver_router

app = FastAPI(title=settings.SERVER_NAME, debug=settings.DEBUG)

app.include_router(driver_router, prefix=f"/api/{settings.API_VERSION}")

instrumentator = Instrumentator().instrument(app)

start_time = time.time()
uptime_metric = Counter("app_uptime_seconds", "Application Uptime in Seconds")


# Function to update the uptime metric
async def update_uptime() -> None:
    while True:
        uptime_metric.inc(1)
        await asyncio.sleep(1)


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.on_event("startup")
async def startup() -> None:
    instrumentator.expose(app)
    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    loop.run_in_executor(executor, asyncio.run, update_uptime())


class HealthCheckResponse(BaseModel):
    status: str
    details: str


@app.get(
    "/health-check",
    response_model=HealthCheckResponse,
    summary="Database Health Check",
    description="Check if the database is healthy",
)
async def health_check(db: AsyncSession = Depends(get_async_session)) -> HealthCheckResponse:
    try:
        result = await db.execute(text("SELECT 1"))
        if result.scalar() == 1:
            return HealthCheckResponse(status="ok", details="Database is healthy")
        else:
            raise HTTPException(status_code=500, detail="Database health check failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database health check failed: {e}") from e


@app.get("/")
async def main() -> dict:
    return {"message": "Hello World"}
