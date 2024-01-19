import os
from ..path import BASE_DIR


HASHING_DEPRECATION: str = 'auto'
HASHING_ALGORITHM: str = "HS256"
SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
UPLOAD_DIR = os.path.join(BASE_DIR, "Uploads")
NUMBER_OF_BYTES = 10
PROJECT_PROTOCOLE = "http"
PROJECT_HOST = "127.0.0.1"
