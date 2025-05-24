import pytest
import json
from unittest.mock import patch, MagicMock
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from app.api.v1.routes.jobs import bp
from app.api.v1.services.jobs import JobService
from app.api.v1.models.jobs import Job


class TestJobRoutes:
    """Test cases for job routes"""

    @pytest.fixture
    def client(self, app):
        """Create test client"""
        app.register_blueprint(bp)
        return app.test_client()

    @pytest.fixture
    def sample_job_data(self):
        """Sample job data for testing"""
        return {
            "title": "Software Engineer",
            "description": "Python developer position",
            "company": "Tech Corp",
            "location": "New York",
            "salary": 100000
        }

    @pytest.fixture
    def sample_job_response(self):
        """Sample job response data"""
        return {
            "id": 1,
            "title": "Software Engineer",
            "description": "Python developer position",
            "company": "Tech Corp",
            "location": "New York",
            "salary": 100000
        }

    def test_create_job_success(self, client, sample_job_data, sample_job_response):
        """Test successful job creation"""
        with patch.object(JobService, 'create_job', return_value=sample_job_response):
            response = client.post('/api/v1/jobs/',
                                   data=json.dumps(sample_job_data),
                                   content_type='application/json')

            assert response.status_code == 201
            data = json.loads(response.data)
            assert data['message'] == "Job created successfully"
            assert data['data'] == sample_job_response

    def test_create_job_validation_error(self, client, sample_job_data):
        """Test job creation with validation error"""
        with patch.object(JobService, 'create_job',
                          side_effect=ValidationError("Title is required")):
            response = client.post('/api/v1/jobs/',
                                   data=json.dumps(sample_job_data),
                                   content_type='application/json')

            assert response.status_code == 400
            # Check if response has either 'error' or 'message' key
            data = json.loads(response.data)
            assert 'error' in data or 'message' in data
            if 'error' in data:
                assert "Invalid input" in data['error'] or "Title is required" in str(data['error'])
            else:
                assert "Invalid input" in data['message'] or "Title is required" in str(data['message'])

    def test_create_job_value_error(self, client, sample_job_data):
        """Test job creation with value error"""
        with patch.object(JobService, 'create_job',
                          side_effect=ValueError("Invalid salary")):
            response = client.post('/api/v1/jobs/',
                                   data=json.dumps(sample_job_data),
                                   content_type='application/json')

            assert response.status_code == 400
            data = json.loads(response.data)
            # Handle different possible response structures
            error_message = data.get('error') or data.get('message', '')
            assert "Invalid salary" in str(error_message)

    def test_create_job_unexpected_error(self, client, sample_job_data):
        """Test job creation with unexpected error"""
        with patch.object(JobService, 'create_job',
                          side_effect=Exception("Database connection failed")):
            response = client.post('/api/v1/jobs/',
                                   data=json.dumps(sample_job_data),
                                   content_type='application/json')

            assert response.status_code == 500
            data = json.loads(response.data)
            # Check for error message in any key
            assert 'error' in data or 'message' in data

    def test_list_jobs_success(self, client, sample_job_response):
        """Test successful job listing"""
        jobs_list = [sample_job_response]
        with patch.object(JobService, 'get_all_jobs', return_value=jobs_list):
            response = client.get('/api/v1/jobs/')

            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['message'] == "Jobs fetched successfully"
            assert data['data'] == jobs_list

    def test_list_jobs_error(self, client):
        """Test job listing with error"""
        with patch.object(JobService, 'get_all_jobs',
                          side_effect=Exception("Database error")):
            response = client.get('/api/v1/jobs/')

            assert response.status_code == 500
            data = json.loads(response.data)
            assert 'error' in data or 'message' in data

    def test_get_job_success(self, client, sample_job_response):
        """Test successful job retrieval"""
        with patch.object(JobService, 'get_job', return_value=sample_job_response):
            response = client.get('/api/v1/jobs/1')

            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['message'] == "Job fetched successfully"
            assert data['data'] == sample_job_response

    def test_get_job_not_found(self, client):
        """Test job retrieval when job not found"""
        with patch.object(JobService, 'get_job',
                          side_effect=ValueError("Job not found")):
            response = client.get('/api/v1/jobs/999')

            assert response.status_code == 404
            data = json.loads(response.data)
            error_message = data.get('error') or data.get('message', '')
            assert "Job not found" in str(error_message)

    def test_get_job_unexpected_error(self, client):
        """Test job retrieval with unexpected error"""
        with patch.object(JobService, 'get_job',
                          side_effect=Exception("Database error")):
            response = client.get('/api/v1/jobs/1')

            assert response.status_code == 500
            data = json.loads(response.data)
            assert 'error' in data or 'message' in data

    def test_update_job_success(self, client, sample_job_data, sample_job_response):
        """Test successful job update"""
        with patch.object(JobService, 'update_job', return_value=sample_job_response):
            response = client.put('/api/v1/jobs/1',
                                  data=json.dumps(sample_job_data),
                                  content_type='application/json')

            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['message'] == "Job updated successfully"
            assert data['data'] == sample_job_response

    def test_update_job_validation_error(self, client, sample_job_data):
        """Test job update with validation error"""
        with patch.object(JobService, 'update_job',
                          side_effect=ValidationError("Invalid data")):
            response = client.put('/api/v1/jobs/1',
                                  data=json.dumps(sample_job_data),
                                  content_type='application/json')

            assert response.status_code == 400
            data = json.loads(response.data)
            error_message = data.get('error') or data.get('message', '')
            assert "Invalid" in str(error_message)

    def test_update_job_not_found(self, client, sample_job_data):
        """Test job update when job not found"""
        with patch.object(JobService, 'update_job',
                          side_effect=ValueError("Job not found")):
            response = client.put('/api/v1/jobs/999',
                                  data=json.dumps(sample_job_data),
                                  content_type='application/json')

            assert response.status_code == 404
            data = json.loads(response.data)
            error_message = data.get('error') or data.get('message', '')
            assert "Job not found" in str(error_message)

    def test_delete_job_success(self, client):
        """Test successful job deletion"""
        with patch.object(JobService, 'delete_job', return_value=None):
            response = client.delete('/api/v1/jobs/1')

            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['message'] == "Job deleted successfully"
            assert data['data'] is None

    def test_delete_job_not_found(self, client):
        """Test job deletion when job not found"""
        with patch.object(JobService, 'delete_job',
                          side_effect=ValueError("Job not found")):
            response = client.delete('/api/v1/jobs/999')

            assert response.status_code == 404
            data = json.loads(response.data)
            error_message = data.get('error') or data.get('message', '')
            assert "Job not found" in str(error_message)

    def test_delete_job_unexpected_error(self, client):
        """Test job deletion with unexpected error"""
        with patch.object(JobService, 'delete_job',
                          side_effect=Exception("Database error")):
            response = client.delete('/api/v1/jobs/1')

            assert response.status_code == 500
            data = json.loads(response.data)
            assert 'error' in data or 'message' in data


class TestJobService:
    """Test cases for JobService"""

    @pytest.fixture
    def mock_db_session(self):
        """Mock database session"""
        with patch('app.api.v1.services.jobs.db.session') as mock_session:
            yield mock_session

    @pytest.fixture
    def mock_job_schema(self):
        """Mock job schema"""
        with patch('app.api.v1.services.jobs.job_schema') as mock_schema:
            yield mock_schema

    @pytest.fixture
    def mock_jobs_schema(self):
        """Mock jobs schema for multiple jobs"""
        with patch('app.api.v1.services.jobs.jobs_schema') as mock_schema:
            yield mock_schema

    @pytest.fixture
    def sample_job_data(self):
        """Sample job data"""
        return {
            "title": "Software Engineer",
            "description": "Python developer position",
            "company": "Tech Corp"
        }

    @pytest.fixture
    def sample_job_model(self):
        """Sample job model instance"""
        job = MagicMock(spec=Job)
        job.id = 1
        job.title = "Software Engineer"
        job.description = "Python developer position"
        job.company = "Tech Corp"
        return job

    def test_create_job_success(self, mock_db_session, mock_job_schema, sample_job_data, sample_job_model):
        """Test successful job creation"""
        mock_job_schema.load.return_value = sample_job_data
        mock_job_schema.dump.return_value = sample_job_data

        with patch('app.api.v1.services.jobs.Job') as mock_job_class:
            mock_job_class.return_value = sample_job_model

            result = JobService.create_job(sample_job_data)

            mock_job_schema.load.assert_called_once_with(sample_job_data)
            mock_job_class.assert_called_once_with(**sample_job_data)
            mock_db_session.add.assert_called_once_with(sample_job_model)
            mock_db_session.commit.assert_called_once()
            mock_job_schema.dump.assert_called_once_with(sample_job_model)
            assert result == sample_job_data

    def test_create_job_validation_error(self, mock_job_schema, sample_job_data):
        """Test job creation with validation error"""
        mock_job_schema.load.side_effect = ValidationError("Title is required")

        with pytest.raises(ValidationError):
            JobService.create_job(sample_job_data)

    def test_create_job_database_error(self, mock_db_session, mock_job_schema, sample_job_data, sample_job_model):
        """Test job creation with database error"""
        mock_job_schema.load.return_value = sample_job_data
        mock_db_session.commit.side_effect = SQLAlchemyError("Database error")

        with patch('app.api.v1.services.jobs.Job') as mock_job_class:
            mock_job_class.return_value = sample_job_model

            with pytest.raises(Exception, match="Failed to create job"):
                JobService.create_job(sample_job_data)

            mock_db_session.rollback.assert_called_once()

    def test_get_all_jobs_success(self, mock_jobs_schema):
        """Test successful retrieval of all jobs"""
        mock_jobs = [MagicMock(), MagicMock()]
        expected_result = [{"id": 1}, {"id": 2}]
        mock_jobs_schema.dump.return_value = expected_result

        with patch('app.api.v1.services.jobs.Job') as mock_job_class:
            mock_job_class.query.all.return_value = mock_jobs

            result = JobService.get_all_jobs()

            mock_job_class.query.all.assert_called_once()
            mock_jobs_schema.dump.assert_called_once_with(mock_jobs)
            assert result == expected_result

    def test_get_all_jobs_database_error(self):
        """Test get all jobs with database error"""
        with patch('app.api.v1.services.jobs.Job') as mock_job_class:
            mock_job_class.query.all.side_effect = SQLAlchemyError("Database error")

            with pytest.raises(Exception, match="Failed to fetch jobs"):
                JobService.get_all_jobs()

    def test_get_job_success(self, mock_job_schema, sample_job_model):
        """Test successful job retrieval by ID"""
        expected_result = {"id": 1, "title": "Software Engineer"}
        mock_job_schema.dump.return_value = expected_result

        with patch('app.api.v1.services.jobs.Job') as mock_job_class:
            mock_job_class.query.get.return_value = sample_job_model

            result = JobService.get_job(1)

            mock_job_class.query.get.assert_called_once_with(1)
            mock_job_schema.dump.assert_called_once_with(sample_job_model)
            assert result == expected_result

    def test_get_job_not_found(self):
        """Test job retrieval when job doesn't exist"""
        with patch('app.api.v1.services.jobs.Job') as mock_job_class:
            mock_job_class.query.get.return_value = None

            with pytest.raises(ValueError, match="Job not found"):
                JobService.get_job(999)

    def test_update_job_success(self, mock_db_session, mock_job_schema, sample_job_model, sample_job_data):
        """Test successful job update"""
        expected_result = {"id": 1, "title": "Updated Engineer"}
        mock_job_schema.load.return_value = sample_job_data
        mock_job_schema.dump.return_value = expected_result

        with patch('app.api.v1.services.jobs.Job') as mock_job_class:
            mock_job_class.query.get.return_value = sample_job_model

            result = JobService.update_job(1, sample_job_data)

            mock_job_class.query.get.assert_called_once_with(1)
            mock_job_schema.load.assert_called_once_with(sample_job_data, partial=True)
            mock_db_session.commit.assert_called_once()
            mock_job_schema.dump.assert_called_once_with(sample_job_model)
            assert result == expected_result

    def test_update_job_not_found(self, sample_job_data):
        """Test job update when job doesn't exist"""
        with patch('app.api.v1.services.jobs.Job') as mock_job_class:
            mock_job_class.query.get.return_value = None

            with pytest.raises(ValueError, match="Job not found"):
                JobService.update_job(999, sample_job_data)

    def test_update_job_validation_error(self, mock_job_schema, sample_job_model, sample_job_data):
        """Test job update with validation error"""
        mock_job_schema.load.side_effect = ValidationError("Invalid data")

        with patch('app.api.v1.services.jobs.Job') as mock_job_class:
            mock_job_class.query.get.return_value = sample_job_model

            with pytest.raises(ValidationError):
                JobService.update_job(1, sample_job_data)

    def test_update_job_database_error(self, mock_db_session, mock_job_schema, sample_job_model, sample_job_data):
        """Test job update with database error"""
        mock_job_schema.load.return_value = sample_job_data
        mock_db_session.commit.side_effect = SQLAlchemyError("Database error")

        with patch('app.api.v1.services.jobs.Job') as mock_job_class:
            mock_job_class.query.get.return_value = sample_job_model

            with pytest.raises(Exception, match="Failed to update job"):
                JobService.update_job(1, sample_job_data)

            mock_db_session.rollback.assert_called_once()

    def test_delete_job_success(self, mock_db_session, sample_job_model):
        """Test successful job deletion"""
        with patch('app.api.v1.services.jobs.Job') as mock_job_class:
            mock_job_class.query.get.return_value = sample_job_model

            JobService.delete_job(1)

            mock_job_class.query.get.assert_called_once_with(1)
            mock_db_session.delete.assert_called_once_with(sample_job_model)
            mock_db_session.commit.assert_called_once()

    def test_delete_job_not_found(self):
        """Test job deletion when job doesn't exist"""
        with patch('app.api.v1.services.jobs.Job') as mock_job_class:
            mock_job_class.query.get.return_value = None

            with pytest.raises(ValueError, match="Job not found"):
                JobService.delete_job(999)

    def test_delete_job_database_error(self, mock_db_session, sample_job_model):
        """Test job deletion with database error"""
        mock_db_session.commit.side_effect = SQLAlchemyError("Database error")

        with patch('app.api.v1.services.jobs.Job') as mock_job_class:
            mock_job_class.query.get.return_value = sample_job_model

            with pytest.raises(Exception, match="Failed to delete job"):
                JobService.delete_job(1)

            mock_db_session.rollback.assert_called_once()


# Conftest.py content for Flask app fixture
@pytest.fixture
def app():
    """Create Flask app for testing"""
    from flask import Flask
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app