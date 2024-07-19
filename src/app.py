from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from driver.routers import driver_router

app = FastAPI(title=settings.SERVER_NAME, debug=settings.DEBUG)

app.include_router(driver_router, prefix=f"/api/{settings.API_VERSION}")

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
async def main() -> dict:
    return {"message": "Hello World"}
