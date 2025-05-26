import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Secret key for Flask sessions
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")

    # PostgreSQL connection string
    DB_TYPE = os.getenv("DB_TYPE", "postgresql")
    POSTGRES_USER = os.getenv("POSTGRES_USER", "your-postgres-db-user")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "your-postgres-db-password")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB", "your-postgres-db-name")

    # SQLAlchemy Database URI for PostgreSQL
    SQLALCHEMY_DATABASE_URI = (
        f"{DB_TYPE}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Threshold for low stock alerts
    LOW_STOCK_THRESHOLD=int(10)


# Initialize config object
config = Config()