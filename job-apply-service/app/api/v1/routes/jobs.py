import logging
from fastapi import APIRouter, Depends, status


from app.api.v1.services.jobs import JobApplicationService
from app.api.v1.schemas.jobs import ApplyJobSchema, JobApplicationResponse, JobApplicationDeleteResponse
from app.api.utils.get_service_class import get_service
from app.api.utils.get_current_user import get_current_user
from app.api.utils.error_response import error_response
from app.api.utils.success_response import success_response

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/applications", tags=["Job Applications"])

@router.post("/apply", status_code=status.HTTP_201_CREATED, response_model=JobApplicationResponse)
async def apply_for_job(
    job_data: ApplyJobSchema,
    service: JobApplicationService = Depends(get_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Apply for a job by providing job ID.

    This endpoint fetches job details from the Flask microservice and creates
    a job application record with user information from Kong gateway.
    """
    try:
        logger.info(f"API request to apply for job ID: {job_data.job_id} by user {current_user['user_id']}")

        applied_job = await service.apply_job(
            job_data,
            current_user["user_id"],
            current_user["user_email"]
        )

        if not applied_job:
            return error_response(status.HTTP_404_NOT_FOUND, "Job not found")

        validated_data = JobApplicationResponse.model_validate(applied_job).model_dump(mode="json")
        return success_response(status.HTTP_201_CREATED, "Job application submitted successfully", validated_data)

    except ValueError as e:
        logger.warning(f"Validation error applying for job: {str(e)}")
        return error_response(status.HTTP_400_BAD_REQUEST, str(e))

    except Exception as e:
        logger.error(f"API error applying for job: {str(e)}")
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to apply for job")


@router.delete("/{application_id}", status_code=status.HTTP_200_OK, response_model=JobApplicationDeleteResponse)
async def delete_applied_job(
    application_id: int,
    service: JobApplicationService = Depends(get_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a job application.

    Permanently removes the job application from records for the authenticated user.
    Only the user who created the application can delete it.
    """
    try:
        logger.info(f"API request to delete job application ID: {application_id} by user {current_user['user_id']}")

        deleted = await service.delete_applied_job(application_id, current_user["user_id"])
        if not deleted:
            return error_response(status.HTTP_404_NOT_FOUND, "Job application not found")

        return success_response(status.HTTP_200_OK, "Job application deleted successfully", None)

    except Exception as e:
        logger.error(f"API error deleting job application {application_id}: {str(e)}")
        return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete job application")
