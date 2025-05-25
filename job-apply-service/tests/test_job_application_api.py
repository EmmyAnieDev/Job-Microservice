import pytest
from unittest.mock import Mock, AsyncMock, patch
from fastapi import status

from app.api.v1.services.jobs import JobApplicationService
from app.api.v1.models.jobs import JobApplication
from app.api.v1.schemas.jobs import ApplyJobSchema


class TestJobApplicationAPI:
    """Test cases for Job Application API endpoints"""

    @pytest.fixture
    def mock_service(self):
        """Mock JobApplicationService"""
        return Mock(spec=JobApplicationService)

    @pytest.fixture
    def mock_current_user(self):
        """Mock current user data"""
        return {
            "user_id": 1,
            "user_email": "test@example.com"
        }

    @pytest.fixture
    def sample_job_application(self):
        """Sample job application for testing"""
        return JobApplication(
            id=1,
            job_id=1,
            user_id=1,
            user_email="test@example.com",
            title="Software Engineer",
            description="Develop awesome software",
            company="TechCorp",
            location="San Francisco",
            salary="$100,000"
        )

    @pytest.mark.asyncio
    async def test_apply_for_job_success(self, mock_service, mock_current_user, sample_job_application):
        """Test successful job application API call"""
        job_data = ApplyJobSchema(job_id=1)
        mock_service.apply_job = AsyncMock(return_value=sample_job_application)

        # Patch the response functions where they're imported in the routes module
        with patch('app.api.v1.routes.jobs.success_response') as mock_success:
            with patch('app.api.v1.routes.jobs.JobApplicationResponse') as mock_response:
                mock_response.model_validate.return_value.model_dump.return_value = {
                    "id": 1,
                    "job_id": 1,
                    "title": "Software Engineer"
                }
                mock_success.return_value = {"status": "success"}

                # Import the function after patching
                from app.api.v1.routes.jobs import apply_for_job
                result = await apply_for_job(job_data, mock_service, mock_current_user)

                mock_service.apply_job.assert_called_once_with(
                    job_data, 1, "test@example.com"
                )
                mock_success.assert_called_once_with(
                    status.HTTP_201_CREATED,
                    "Job application submitted successfully",
                    {"id": 1, "job_id": 1, "title": "Software Engineer"}
                )

    @pytest.mark.asyncio
    async def test_apply_for_job_not_found(self, mock_service, mock_current_user):
        """Test job application when job not found"""
        job_data = ApplyJobSchema(job_id=999)
        mock_service.apply_job = AsyncMock(return_value=None)

        with patch('app.api.v1.routes.jobs.error_response') as mock_error:
            mock_error.return_value = {"error": "Job not found"}

            from app.api.v1.routes.jobs import apply_for_job
            result = await apply_for_job(job_data, mock_service, mock_current_user)

            mock_error.assert_called_once_with(
                status.HTTP_404_NOT_FOUND, "Job not found"
            )

    @pytest.mark.asyncio
    async def test_apply_for_job_validation_error(self, mock_service, mock_current_user):
        """Test job application with validation error"""
        job_data = ApplyJobSchema(job_id=1)
        mock_service.apply_job = AsyncMock(side_effect=ValueError("Already applied"))

        with patch('app.api.v1.routes.jobs.error_response') as mock_error:
            mock_error.return_value = {"error": "Already applied"}

            from app.api.v1.routes.jobs import apply_for_job
            result = await apply_for_job(job_data, mock_service, mock_current_user)

            mock_error.assert_called_once_with(
                status.HTTP_400_BAD_REQUEST, "Already applied"
            )

    @pytest.mark.asyncio
    async def test_apply_for_job_server_error(self, mock_service, mock_current_user):
        """Test job application with server error"""
        job_data = ApplyJobSchema(job_id=1)
        mock_service.apply_job = AsyncMock(side_effect=Exception("Server error"))

        with patch('app.api.v1.routes.jobs.error_response') as mock_error:
            mock_error.return_value = {"error": "Failed to apply for job"}

            from app.api.v1.routes.jobs import apply_for_job
            result = await apply_for_job(job_data, mock_service, mock_current_user)

            mock_error.assert_called_once_with(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to apply for job"
            )

    @pytest.mark.asyncio
    async def test_delete_applied_job_success(self, mock_service, mock_current_user):
        """Test successful job application deletion"""
        mock_service.delete_applied_job = AsyncMock(return_value=True)

        with patch('app.api.v1.routes.jobs.success_response') as mock_success:
            mock_success.return_value = {"status": "success"}

            from app.api.v1.routes.jobs import delete_applied_job
            result = await delete_applied_job(1, mock_service, mock_current_user)

            mock_service.delete_applied_job.assert_called_once_with(1, 1)
            mock_success.assert_called_once_with(
                status.HTTP_200_OK, "Job application deleted successfully", None
            )

    @pytest.mark.asyncio
    async def test_delete_applied_job_not_found(self, mock_service, mock_current_user):
        """Test deletion of non-existent job application"""
        mock_service.delete_applied_job = AsyncMock(return_value=False)

        with patch('app.api.v1.routes.jobs.error_response') as mock_error:
            mock_error.return_value = {"error": "Job application not found"}

            from app.api.v1.routes.jobs import delete_applied_job
            result = await delete_applied_job(999, mock_service, mock_current_user)

            mock_error.assert_called_once_with(
                status.HTTP_404_NOT_FOUND, "Job application not found"
            )

    @pytest.mark.asyncio
    async def test_delete_applied_job_server_error(self, mock_service, mock_current_user):
        """Test job application deletion with server error"""
        mock_service.delete_applied_job = AsyncMock(side_effect=Exception("Server error"))

        with patch('app.api.v1.routes.jobs.error_response') as mock_error:
            mock_error.return_value = {"error": "Failed to delete job application"}

            from app.api.v1.routes.jobs import delete_applied_job
            result = await delete_applied_job(1, mock_service, mock_current_user)

            mock_error.assert_called_once_with(
                status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to delete job application"
            )
