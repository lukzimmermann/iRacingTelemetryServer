import os
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from routes.telemetryFile import telemetryFileService
from utils.auth_bearer import JWTBearer

router = APIRouter(prefix="/telemetry-file", tags=["TelemetryFile"])
auth_dependency = JWTBearer()

@router.post("/")
async def upload_file(file: UploadFile = File(...), token: str = Depends(auth_dependency)):
    response = await telemetryFileService.save_telemetry_file(file)
    return response

@router.get("/test")
async def test(token: str = Depends(auth_dependency)):
    return {"value": "test"}