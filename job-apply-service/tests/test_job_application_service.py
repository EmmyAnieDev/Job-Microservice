import pytest
from unittest.mock import Mock, AsyncMock, patch
from sqlalchemy.orm import Session
from httpx import Response

from app.api.v1.services.jobs import JobApplicationService
from app.api.v1.models.jobs import JobApplication
from app.api.v1.schemas.jobs import ApplyJobSchema


class TestJobApplicationService:
    """Test cases for JobApplicationService"""

    @pytest.fixture
    def mock_db(self):
        """Mock database session"""
        return Mock(spec=Session)

    @pytest.fixture
    def service(self, mock_db):
        """Create JobApplicationService instance with mocked dependencies"""
        return JobApplicationService(db=mock_db, flask_service_url="http://test-flask-service")

    @pytest.fixture
    def sample_job_data(self):
        """Sample job data for testing"""
        return {
            "id": 1,
            "title": "Software Engineer",
            "description": "Develop awesome software",
            "company": "TechCorp",
            "location": "San Francisco",
            "salary": "$100,000"
        }

    @pytest.fixture
    def sample_apply_schema(self):
        """Sample ApplyJobSchema for testing"""
        return ApplyJobSchema(job_id=1)

    @pytest.mark.asyncio
    async def test_get_job_details_success(self, service, sample_job_data):
        """Test successful job details fetch"""
        # Mock HTTP response
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": sample_job_data}

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)

            result = await service.get_job_details(1)

            assert result == sample_job_data
            mock_client.return_value.__aenter__.return_value.get.assert_called_once_with(
                "http://test-flask-service/api/v1/jobs/1"
            )

    @pytest.mark.asyncio
    async def test_get_job_details_not_found(self, service):
        """Test job details fetch when job not found"""
        mock_response = Mock(spec=Response)
        mock_response.status_code = 404

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)

            result = await service.get_job_details(999)

            assert result is None

    @pytest.mark.asyncio
    async def test_get_job_details_server_error(self, service):
        """Test job details fetch with server error"""
        mock_response = Mock(spec=Response)
        mock_response.status_code = 500

        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(return_value=mock_response)

            result = await service.get_job_details(1)

            assert result is None

    @pytest.mark.asyncio
    async def test_get_job_details_exception(self, service):
        """Test job details fetch with network exception"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get = AsyncMock(
                side_effect=Exception("Network error")
            )

            result = await service.get_job_details(1)

            assert result is None

    @pytest.mark.asyncio
    async def test_apply_job_success(self, service, mock_db, sample_apply_schema, sample_job_data):
        """Test successful job application"""
        # Mock no existing application
        mock_db.query.return_value.filter.return_value.first.return_value = None

        # Mock job details fetch
        with patch.object(service, 'get_job_details', return_value=sample_job_data):
            # Mock database operations
            mock_db.add = Mock()
            mock_db.commit = Mock()
            mock_db.refresh = Mock()

            result = await service.apply_job(sample_apply_schema, user_id=1, user_email="test@example.com")

            # Verify database operations
            mock_db.add.assert_called_once()
            mock_db.commit.assert_called_once()
            mock_db.refresh.assert_called_once()

            # Verify the job application was created with correct data
            added_job = mock_db.add.call_args[0][0]
            assert isinstance(added_job, JobApplication)
            assert added_job.job_id == 1
            assert added_job.user_id == 1
            assert added_job.user_email == "test@example.com"
            assert added_job.title == sample_job_data["title"]
            assert added_job.company == sample_job_data["company"]

    @pytest.mark.asyncio
    async def test_apply_job_already_applied(self, service, mock_db, sample_apply_schema):
        """Test applying for job when already applied"""
        # Mock existing application
        existing_app = JobApplication(job_id=1, user_id=1)
        mock_db.query.return_value.filter.return_value.first.return_value = existing_app

        with pytest.raises(ValueError, match="You have already applied for this job"):
            await service.apply_job(sample_apply_schema, user_id=1, user_email="test@example.com")

    @pytest.mark.asyncio
    async def test_apply_job_not_found(self, service, mock_db, sample_apply_schema):
        """Test applying for non-existent job"""
        # Mock no existing application
        mock_db.query.return_value.filter.return_value.first.return_value = None

        # Mock job not found
        with patch.object(service, 'get_job_details', return_value=None):
            result = await service.apply_job(sample_apply_schema, user_id=1, user_email="test@example.com")

            assert result is None

    @pytest.mark.asyncio
    async def test_apply_job_database_error(self, service, mock_db, sample_apply_schema, sample_job_data):
        """Test job application with database error"""
        # Mock no existing application
        mock_db.query.return_value.filter.return_value.first.return_value = None

        # Mock job details fetch
        with patch.object(service, 'get_job_details', return_value=sample_job_data):
            # Mock database error
            mock_db.add = Mock()
            mock_db.commit = Mock(side_effect=Exception("Database error"))
            mock_db.rollback = Mock()

            with pytest.raises(Exception, match="Database error"):
                await service.apply_job(sample_apply_schema, user_id=1, user_email="test@example.com")

            mock_db.rollback.assert_called_once()

    def test_get_applied_job_success(self, service, mock_db):
        """Test successful retrieval of applied job"""
        mock_application = JobApplication(id=1, job_id=1, user_id=1)
        mock_db.query.return_value.filter.return_value.first.return_value = mock_application

        result = service.get_applied_job(application_id=1, user_id=1)

        assert result == mock_application
        mock_db.query.assert_called_once_with(JobApplication)

    def test_get_applied_job_not_found(self, service, mock_db):
        """Test retrieval of non-existent applied job"""
        mock_db.query.return_value.filter.return_value.first.return_value = None

        result = service.get_applied_job(application_id=999, user_id=1)

        assert result is None

    @pytest.mark.asyncio
    async def test_delete_applied_job_success(self, service, mock_db):
        """Test successful deletion of applied job"""
        mock_application = JobApplication(id=1, job_id=1, user_id=1)

        with patch.object(service, 'get_applied_job', return_value=mock_application):
            mock_db.delete = Mock()
            mock_db.commit = Mock()

            result = await service.delete_applied_job(application_id=1, user_id=1)

            assert result is True
            mock_db.delete.assert_called_once_with(mock_application)
            mock_db.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_applied_job_not_found(self, service, mock_db):
        """Test deletion of non-existent applied job"""
        with patch.object(service, 'get_applied_job', return_value=None):
            result = await service.delete_applied_job(application_id=999, user_id=1)

            assert result is False

    @pytest.mark.asyncio
    async def test_delete_applied_job_database_error(self, service, mock_db):
        """Test job application deletion with database error"""
        mock_application = JobApplication(id=1, job_id=1, user_id=1)

        with patch.object(service, 'get_applied_job', return_value=mock_application):
            mock_db.delete = Mock()
            mock_db.commit = Mock(side_effect=Exception("Database error"))
            mock_db.rollback = Mock()

            with pytest.raises(Exception, match="Database error"):
                await service.delete_applied_job(application_id=1, user_id=1)

            mock_db.rollback.assert_called_once()
