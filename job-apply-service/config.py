import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Use this to build paths inside the project
BASE_DIR = Path(__file__).resolve().parent

class Config:

    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

    APP_PORT: int = int(os.getenv("APP_PORT", 8081))

    DB_TYPE = os.getenv("DB_TYPE", "postgresql")
    DB_USER = os.getenv("DB_USER", "your-postgres-db-user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "your-postgres-db-password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "your-postgres-db-name")


# Initialize config object
config = Config()