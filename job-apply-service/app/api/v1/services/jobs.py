import logging
import httpx
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any

from app.api.v1.models.jobs import JobApplication
from app.api.v1.schemas.jobs import ApplyJobSchema
from config import config


logger = logging.getLogger(__name__)


class JobApplicationService:
    """Service for job application operations"""

    def __init__(self, db: Session, flask_service_url: str = config.JOB_LISTING_BASE_URL):
        self.db = db
        self.flask_service_url = flask_service_url


    async def get_job_details(self, job_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch job details from Flask microservice.

        Args:
            job_id: ID of the job to fetch

        Returns:
            Job details dictionary or None if not found
        """
        try:
            logger.info(f"Fetching job details for job ID: {job_id} from Flask services")

            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.flask_service_url}/api/v1/jobs/{job_id}")

                if response.status_code == 200:
                    response_json = response.json()
                    job_data = response_json.get("data")
                    logger.info(f"Successfully fetched job details for job ID: {job_id}")
                    return job_data
                elif response.status_code == 404:
                    logger.warning(f"Job with ID {job_id} not found in Flask services")
                    return None
                else:
                    logger.error(f"Failed to fetch job details: HTTP {response.status_code}")
                    return None

        except Exception as e:
            logger.error(f"Error fetching job details for job ID {job_id}: {str(e)}")
            return None


    async def apply_job(self, job_data: ApplyJobSchema, user_id: int, user_email: str) -> Optional[JobApplication]:
        """
        Apply for a job by fetching details from Flask services.

        Args:
            job_data: Job application data containing job_id
            user_id: ID of the user applying
            user_email: Email of the user applying

        Returns:
            Created job application or None if job not found
        """
        try:
            logger.info(f"User {user_id} ({user_email}) applying for job ID: {job_data.job_id}")

            # Check if user already applied for this job
            existing_application = self.db.query(JobApplication).filter(
                JobApplication.job_id == job_data.job_id,
                JobApplication.user_id == user_id
            ).first()

            if existing_application:
                logger.warning(f"User {user_id} already applied for job ID: {job_data.job_id}")
                raise ValueError("You have already applied for this job")

            # Fetch job details from Flask services
            job_details = await self.get_job_details(job_data.job_id)
            if not job_details:
                logger.warning(f"Job with ID {job_data.job_id} not found")
                return None

            # Create job application with fetched details
            db_job = JobApplication(
                job_id=job_data.job_id,
                user_id=user_id,
                user_email=user_email,
                title=job_details.get('title'),
                description=job_details.get('description'),
                company=job_details.get('company'),
                location=job_details.get('location'),
                salary=job_details.get('salary')
            )

            self.db.add(db_job)
            self.db.commit()
            self.db.refresh(db_job)

            logger.info(f"Successfully applied for job with application ID: {db_job.id} for user {user_id}")
            return db_job

        except ValueError:
            # Re-raise validation errors
            raise
        except Exception as e:
            logger.error(f"Failed to apply for job for user {user_id}: {str(e)}")
            self.db.rollback()
            raise


    def get_applied_job(self, application_id: int, user_id: int) -> Optional[JobApplication]:
        """
        Get applied job by application ID for specific user.

        Args:
            application_id: Job application ID
            user_id: User ID to verify ownership

        Returns:
            Job application if found and belongs to user
        """
        logger.debug(f"Getting job application with ID: {application_id} for user {user_id}")
        application = self.db.query(JobApplication).filter(
            JobApplication.id == application_id,
            JobApplication.user_id == user_id
        ).first()

        if not application:
            logger.warning(f"Job application with ID {application_id} not found for user {user_id}")

        return application


    async def delete_applied_job(self, application_id: int, user_id: int) -> bool:
        """
        Delete applied job for specific user.

        Args:
            application_id: Job application ID to delete
            user_id: User ID to verify ownership

        Returns:
            True if deleted, False if not found or doesn't belong to user
        """
        try:
            logger.info(f"User {user_id} deleting job application with ID: {application_id}")

            db_application = self.get_applied_job(application_id, user_id)
            if not db_application:
                return False

            self.db.delete(db_application)
            self.db.commit()

            logger.info(f"Successfully deleted job application with ID: {application_id} for user {user_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete job application {application_id} for user {user_id}: {str(e)}")
            self.db.rollback()
            raise

