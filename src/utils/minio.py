import os
import io 
from dotenv import load_dotenv
from fastapi import UploadFile
from sqlalchemy import create_engine
from utils.singleton import singleton
from sqlalchemy.orm import sessionmaker
from minio import Minio

load_dotenv()

MINIO_BUCKET = str(os.getenv('MINIO_BUCKET'))

@singleton
class MinioService():
    def __init__(self) -> None:
        self.session = Minio( str(os.getenv('MINIO_HOST')),
            access_key = str(os.getenv('MINIO_ACCESS_KEY')),
            secret_key = str(os.getenv('MINIO_SECRET_KEY')),
            secure = False,
        )

    def get_session(self):
        return self.session
    
    def upload_file(self, file: UploadFile):
        print("SESSION KEY: ", str(os.getenv('MINIO_ACCESS_KEY')))
        file_content = file.file.read()
        file_size = len(file_content)

        result = self.session.put_object(
            bucket_name=MINIO_BUCKET,
            object_name=file.filename,
            data=io.BytesIO(file_content),
            length=file_size,
            part_size=10 * 1024 * 1024,
        )

        print(
            f"Created {result.object_name} object; etag: {result.etag}, version-id: {result.version_id}"
        )
