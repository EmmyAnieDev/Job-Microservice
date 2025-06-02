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

@router.post("", status_code=status.HTTP_201_CREATED, response_model=JobApplicationResponse)
async def apply_for_job(
    job_data: ApplyJobSchema,
    service: JobApplicationService = Depends(get_service),
    current_user: dict = Depends(get_current_user)
):
    """
    Apply for a job.

    This endpoint allows an authenticated user to apply for a job using a job ID.
    It retrieves job details from the Flask microservice and creates a job application record.

    Args:
        job_data (ApplyJobSchema): Data containing the job ID and any additional application information.
        service (JobApplicationService): Dependency that handles job application logic.
        current_user (dict): Dictionary containing authenticated user's information (`user_id` and `user_email`).

    Returns:
        JSONResponse:
            - HTTP_201_CREATED with success message and application data if job is successfully applied for.
            - HTTP_404_NOT_FOUND if the job does not exist.
            - HTTP_400_BAD_REQUEST for validation errors.
            - HTTP_500_INTERNAL_SERVER_ERROR for unexpected server errors.
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

    This endpoint allows an authenticated user to delete a previously submitted job application.
    Only the user who created the application can delete it.

    Args:
        application_id (int): The unique ID of the job application to be deleted.
        service (JobApplicationService): Dependency that handles deletion logic.
        current_user (dict): Dictionary containing authenticated user's information (`user_id`).

    Returns:
        JSONResponse:
            - HTTP_200_OK with success message if deletion is successful.
            - HTTP_404_NOT_FOUND if the job application does not exist or does not belong to the user.
            - HTTP_500_INTERNAL_SERVER_ERROR for unexpected server errors.
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
