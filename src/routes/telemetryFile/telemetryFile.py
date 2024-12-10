from fastapi import APIRouter
from routes.telemetryFile import telemetryFileService

router = APIRouter(prefix="/telemetry-file", tags=["TelemetryFile"])

@router.get("/")
async def root():
    return telemetryFileService.say_hello()