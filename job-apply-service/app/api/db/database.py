""" The database module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from config import BASE_DIR, config

DB_HOST = config.DB_HOST
DB_PORT = config.DB_PORT
DB_USER = config.DB_USER
DB_PASSWORD = config.DB_PASSWORD
DB_NAME = config.DB_NAME
DB_TYPE = config.DB_TYPE


def get_db_engine(test_mode: bool = False):
    if DB_TYPE == "sqlite" or test_mode:
        # For SQLite, use a file in the project root
        if test_mode:
            # Use a test-specific database file
            DATABASE_URL = f"sqlite:///{BASE_DIR}/test.db"
        else:
            # Check for DATABASE_URL in config (from environment variables)
            if hasattr(config, 'database_url') and config.database_url:
                DATABASE_URL = config.database_url
            else:
                DATABASE_URL = f"sqlite:///{BASE_DIR}/db.sqlite3"

        # Always use check_same_thread=False for SQLite
        return create_engine(
            DATABASE_URL, connect_args={"check_same_thread": False}
        )
    elif DB_TYPE == "postgresql":
        # For PostgreSQL, construct the connection string from components
        DATABASE_URL = (
            f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        )
        return create_engine(DATABASE_URL)
    else:
        # Default to SQLite if DB_TYPE is not recognized
        DATABASE_URL = f"sqlite:///{BASE_DIR}/db.sqlite3"
        return create_engine(
            DATABASE_URL, connect_args={"check_same_thread": False}
        )


engine = get_db_engine()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_session = scoped_session(SessionLocal)

Base = declarative_base()


def create_database():
    return Base.metadata.create_all(bind=engine)


def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()