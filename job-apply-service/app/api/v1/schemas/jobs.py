from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ApplyJobSchema(BaseModel):
    """Schema for applying to a job"""
    job_id: int


class JobApplicationResponse(BaseModel):
    """Response schema for job application"""
    id: int
    job_id: int
    user_id: int
    user_email: str
    title: str
    description: Optional[str] = None
    company: str
    location: Optional[str] = None
    salary: Optional[float] = None
    applied_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class JobApplicationDeleteResponse(BaseModel):
    status: str
    message: str