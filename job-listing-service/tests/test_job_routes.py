import pytest
import json
from unittest.mock import patch

from marshmallow import ValidationError

from app.api.v1.routes.jobs import bp
from app.api.v1.services.jobs import JobService


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
            response = client.post('/api/v1/jobs',
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
            response = client.post('/api/v1/jobs',
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
            response = client.post('/api/v1/jobs',
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
            response = client.post('/api/v1/jobs',
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
            response = client.get('/api/v1/jobs')

            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['message'] == "Jobs fetched successfully"
            assert data['data'] == jobs_list

    def test_list_jobs_error(self, client):
        """Test job listing with error"""
        with patch.object(JobService, 'get_all_jobs',
                          side_effect=Exception("Database error")):
            response = client.get('/api/v1/jobs')

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

