from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.v1.services.jobs import JobApplicationService
from app.api.db.database import get_db

def get_service(db: Session = Depends(get_db)) -> JobApplicationService:
    return JobApplicationService(db)
