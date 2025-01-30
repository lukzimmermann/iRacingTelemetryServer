import os
from fastapi import File, HTTPException, UploadFile
from utils.database import Database
from utils.minio import MinioService

sql_session = Database().get_session()
minio_session = MinioService()

UPLOAD_DIRECTORY = "/Users/lukas/Github/iRacingTelemetryServer/telemetry_data"

async def save_telemetry_file(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
    if not file.filename.endswith(".ibt"):
        raise HTTPException(status_code=400, detail="Only .ibt files are allowed.")
    
    minio_session.upload_file(file)

    file_path = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"filename": file.filename, "status": "uploaded successfully"}