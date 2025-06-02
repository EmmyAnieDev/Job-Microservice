from flask import Blueprint, request
from marshmallow import ValidationError
import logging

from app.api.utils.error_response import error_response
from app.api.utils.success_response import success_response
from app.api.v1.services.jobs import JobService

bp = Blueprint('jobs', __name__, url_prefix="/api/v1/jobs")
logger = logging.getLogger(__name__)

@bp.route('', methods=['POST'])
def create_job():
    """
    Create a new job.

    This endpoint creates a job using the JSON payload provided in the request body.

    Args:
        None directly (reads JSON payload from request).

    Returns:
        JSON response:
            - 201 Created with the created job data.
            - 400 Bad Request if input validation fails.
            - 500 Internal Server Error for unexpected issues.
    """
    try:
        data = request.get_json()
        job = JobService.create_job(data)
        return success_response(201, "Job created successfully", job)
    except ValidationError as e:
        logger.error(f"Validation error while creating job: {str(e)}")
        return error_response(400, f"Invalid input: {str(e)}")
    except ValueError as e:
        logger.warning(f"Value error while creating job: {str(e)}")
        return error_response(400, str(e))
    except Exception as e:
        logger.critical(f"Unexpected error while creating job: {str(e)}")
        return error_response(500, "An unexpected error occurred")


@bp.route('', methods=['GET'])
def list_jobs():
    """
    List all jobs.

    Fetches and returns a list of all available jobs.

    Args:
        None

    Returns:
        JSON response:
            - 200 OK with a list of jobs.
            - 500 Internal Server Error for unexpected issues.
    """
    try:
        jobs = JobService.get_all_jobs()
        return success_response(200, "Jobs fetched successfully", jobs)
    except Exception as e:
        logger.critical(f"Unexpected error while listing jobs: {str(e)}")
        return error_response(500, "An unexpected error occurred")


@bp.route('/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """
    Get a specific job by ID.

    Fetches a single job using its unique identifier.

    Args:
        job_id (int): The unique ID of the job to retrieve.

    Returns:
        JSON response:
            - 200 OK with the job data.
            - 404 Not Found if the job does not exist.
            - 500 Internal Server Error for unexpected issues.
    """
    try:
        job = JobService.get_job(job_id)
        return success_response(200, "Job fetched successfully", job)
    except ValueError as e:
        logger.warning(f"Job not found: {str(e)}")
        return error_response(404, str(e))
    except Exception as e:
        logger.critical(f"Unexpected error while fetching job: {str(e)}")
        return error_response(500, "An unexpected error occurred")


@bp.route('/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    """
    Update a job.

    Updates job details using the provided JSON payload.

    Args:
        job_id (int): The unique ID of the job to update.
        JSON body (dict): The updated job data.

    Returns:
        JSON response:
            - 200 OK with the updated job data.
            - 400 Bad Request for validation errors.
            - 404 Not Found if the job does not exist.
            - 500 Internal Server Error for unexpected issues.
    """
    try:
        data = request.get_json()
        job = JobService.update_job(job_id, data)
        return success_response(200, "Job updated successfully", job)
    except ValidationError as e:
        logger.error(f"Validation error while updating job: {str(e)}")
        return error_response(400, f"Invalid input: {str(e)}")
    except ValueError as e:
        logger.warning(f"Value error while updating job: {str(e)}")
        return error_response(404, str(e))
    except Exception as e:
        logger.critical(f"Unexpected error while updating job: {str(e)}")
        return error_response(500, "An unexpected error occurred")


@bp.route('/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """
    Delete a job.

    Permanently deletes a job from the database.

    Args:
        job_id (int): The unique ID of the job to delete.

    Returns:
        JSON response:
            - 200 OK if deletion is successful.
            - 404 Not Found if the job does not exist.
            - 500 Internal Server Error for unexpected issues.
    """
    try:
        JobService.delete_job(job_id)
        return success_response(200, "Job deleted successfully", None)
    except ValueError as e:
        logger.warning(f"Job not found for deletion: {str(e)}")
        return error_response(404, str(e))
    except Exception as e:
        logger.critical(f"Unexpected error while deleting job: {str(e)}")
        return error_response(500, "An unexpected error occurred")
