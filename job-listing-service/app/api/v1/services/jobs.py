import logging
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from app.api.db import db
from app.api.v1.models.jobs import Job
from app.api.v1.schemas.jobs import JobSchema

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

job_schema = JobSchema()
jobs_schema = JobSchema(many=True)

class JobService:

    @staticmethod
    def create_job(data):
        """Create a new job."""
        try:
            job_data = job_schema.load(data)
            job = Job(**job_data)
            db.session.add(job)
            db.session.commit()
            logger.info(f"Created job with ID {job.id}")
            return job_schema.dump(job)
        except ValidationError as ve:
            logger.error(f"Validation error while creating job: {ve.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error while creating job: {str(e)}")
            raise Exception("Failed to create job")

    @staticmethod
    def get_all_jobs():
        """Get all jobs."""
        try:
            jobs = Job.query.all()
            logger.info(f"Retrieved {len(jobs)} jobs")
            return jobs_schema.dump(jobs)
        except SQLAlchemyError as e:
            logger.error(f"Database error while retrieving jobs: {str(e)}")
            raise Exception("Failed to fetch jobs")

    @staticmethod
    def get_job(job_id):
        """Get a job by ID."""
        job = Job.query.get(job_id)
        if not job:
            logger.warning(f"Job ID {job_id} not found")
            raise ValueError("Job not found")
        logger.info(f"Retrieved job with ID {job_id}")
        return job_schema.dump(job)

    @staticmethod
    def update_job(job_id, data):
        """Update a job by ID."""
        job = Job.query.get(job_id)
        if not job:
            logger.warning(f"Job ID {job_id} not found for update")
            raise ValueError("Job not found")

        try:
            job_data = job_schema.load(data, partial=True)
            for key, value in job_data.items():
                setattr(job, key, value)
            db.session.commit()
            logger.info(f"Updated job with ID {job_id}")
            return job_schema.dump(job)
        except ValidationError as ve:
            logger.error(f"Validation error while updating job: {ve.messages}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error while updating job: {str(e)}")
            raise Exception("Failed to update job")

    @staticmethod
    def delete_job(job_id):
        """Delete a job by ID."""
        job = Job.query.get(job_id)
        if not job:
            logger.warning(f"Job ID {job_id} not found for deletion")
            raise ValueError("Job not found")

        try:
            db.session.delete(job)
            db.session.commit()
            logger.info(f"Deleted job with ID {job_id}")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error while deleting job: {str(e)}")
            raise Exception("Failed to delete job")
