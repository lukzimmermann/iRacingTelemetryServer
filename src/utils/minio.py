import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from utils.singleton import singleton
from sqlalchemy.orm import sessionmaker
from minio import Minio

load_dotenv()

MINIO_BUCKET = str(os.getenv('MINIO_BUCKET'))

@singleton
class Database():
    def __init__(self) -> None:
        self.session = Minio( str(os.getenv('MINIO_HOST')),
            access_key = str(os.getenv('MINIO_ACCESS_KEY')),
            secret_key = str(os.getenv('MINIO_SECRET_KEY')),
            secure = False,
        )

    def get_session(self):
        return self.session
