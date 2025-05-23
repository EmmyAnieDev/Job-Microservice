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

    # Redis URL for token blocklist
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # Mail settings for Flask-Mail
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 465))
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "your-email@gmail.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "your-app-password")
    MAIL_FROM = os.getenv("MAIL_FROM", "your-email@gmail.com")
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "Inventory Management System")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "False").lower() == "true"
    MAIL_USE_SSL = os.getenv("MAIL_USE_SSL", "True").lower() == "true"

    # Celery settings
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

    # Threshold for low stock alerts
    LOW_STOCK_THRESHOLD=int(10)


# Initialize config object
config = Config()