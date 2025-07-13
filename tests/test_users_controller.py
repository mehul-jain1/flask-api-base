import pytest
import json
from unittest.mock import patch
from http import HTTPStatus


@pytest.mark.api
@pytest.mark.auth
class TestUsersController:
    """Test cases for users controller endpoints."""

    def test_create_user_success(self, client, auth_headers, sample_user_data, mock_celery):
        """Test successful user creation."""
        with patch('app.services.users.saver.UserSaver.save') as mock_save:
            # Mock user object
            mock_user = type('MockUser', (), {
                'id': 1,
                'serialize': {'id': 1, 'name': 'Test User', 'email': 'test@example.com'}
            })()
            mock_save.return_value = mock_user
            
            response = client.post('/api/users', json=sample_user_data, headers=auth_headers)
            data = response.get_json()
            
            # Debug: print the response if it's not what we expect
            if response.status_code != HTTPStatus.CREATED:
                print(f"Expected 201, got {response.status_code}")
                print(f"Response data: {data}")
            
            assert response.status_code == HTTPStatus.CREATED
            assert data['status'] == 'success'
            assert 'user' in data
            assert data['user']['id'] == 1
            assert 'job_result' in data
            assert data['job_result']['job_id'] == 'test-task-id'

    def test_create_user_validation_error(self, client, auth_headers):
        """Test user creation with validation errors."""
        invalid_user_data = {
            'name': '',  # Empty name should fail validation
            'email': 'invalid-email',  # Invalid email format
            'role': 'invalid-role'  # Invalid role
        }
        
        response = client.post('/api/users', json=invalid_user_data, headers=auth_headers)
        data = response.get_json()
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert data['status'] == 'failed'
        assert 'message' in data

    def test_create_user_save_failure(self, client, auth_headers, sample_user_data):
        """Test user creation when save fails."""
        with patch('app.controllers.api.v1.users_controller.UserSaver') as mock_user_saver_class:
            # Create a mock instance with the errors attribute
            mock_instance = mock_user_saver_class.return_value
            mock_instance.save.return_value = None
            mock_instance.errors = ['Save failed']
            
            response = client.post('/api/users', json=sample_user_data, headers=auth_headers)
            data = response.get_json()
            
            assert response.status_code == HTTPStatus.BAD_REQUEST
            assert data['status'] == 'failed'
            assert data['message'] == 'User creation failed'

    def test_create_user_unauthorized(self, client, sample_user_data):
        """Test user creation without authentication."""
        response = client.post('/api/users', json=sample_user_data)
        
        assert response.status_code in [HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN]

    def test_get_all_users_success(self, client, auth_headers):
        """Test successful retrieval of all users."""
        response = client.get('/api/users', headers=auth_headers)
        data = response.get_json()
        
        assert response.status_code == HTTPStatus.ACCEPTED
        assert data['status'] == 'success'
        assert 'users' in data
        assert 'pagination' in data
        assert isinstance(data['users'], list)
        assert len(data['users']) >= 0

    def test_get_all_users_with_pagination(self, client, auth_headers):
        """Test user retrieval with pagination parameters."""
        response = client.get('/api/users?pageNumber=1&pageSize=5', headers=auth_headers)
        data = response.get_json()
        
        assert response.status_code == HTTPStatus.ACCEPTED
        assert data['status'] == 'success'
        assert data['pagination']['page'] == 1
        assert data['pagination']['per_page'] == 5

    def test_get_all_users_unauthorized(self, client):
        """Test user retrieval without authentication."""
        response = client.get('/api/users')
        
        assert response.status_code in [HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN]

    def test_get_user_by_id_success(self, client, auth_headers):
        """Test successful retrieval of a specific user."""
        # Use the test user created in conftest (id should be 1 or 2)
        response = client.get('/api/users/1', headers=auth_headers)
        data = response.get_json()
        
        assert response.status_code == HTTPStatus.OK
        assert data['status'] == 'success'
        assert 'user' in data
        assert data['user']['id'] == 1

    def test_get_user_by_id_not_found(self, client, auth_headers):
        """Test retrieval of non-existent user."""
        response = client.get('/api/users/999', headers=auth_headers)
        data = response.get_json()
        
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert data['status'] == 'failed'
        assert data['message'] == 'User record not found'

    def test_get_user_by_id_unauthorized(self, client):
        """Test user retrieval without authentication."""
        response = client.get('/api/users/1')
        
        assert response.status_code in [HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN]

    def test_get_user_by_id_invalid_id(self, client, auth_headers):
        """Test user retrieval with invalid ID format."""
        response = client.get('/api/users/invalid', headers=auth_headers)
        
        # This might return 404 or 400 depending on Flask routing
        assert response.status_code in [HTTPStatus.NOT_FOUND, HTTPStatus.BAD_REQUEST]

    @patch('app.validators.api.schema_validator.SchemaValidator.validate_user_schema')
    def test_create_user_schema_validation_error(self, mock_validate, client, auth_headers):
        """Test user creation with schema validation errors."""
        mock_validate.return_value = ['Schema validation failed']
        
        response = client.post('/api/users', json={}, headers=auth_headers)
        data = response.get_json()
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert data['status'] == 'failed'
        assert 'Schema validation failed' in data['message']

    @patch('app.validators.api.data_validator.DataValidator.validate_data')
    def test_create_user_data_validation_error(self, mock_validate, client, auth_headers, sample_user_data):
        """Test user creation with data validation errors."""
        mock_validate.return_value = ['Data validation failed']
        
        response = client.post('/api/users', json=sample_user_data, headers=auth_headers)
        data = response.get_json()
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert data['status'] == 'errors'
        assert 'Data validation failed' in data['message']

    def test_users_endpoint_methods(self, client, auth_headers):
        """Test allowed methods for users endpoint."""
        # Test unsupported methods
        response = client.put('/api/users', headers=auth_headers)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        
        response = client.delete('/api/users', headers=auth_headers)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_user_by_id_endpoint_methods(self, client, auth_headers):
        """Test allowed methods for user by ID endpoint."""
        # Test unsupported methods
        response = client.post('/api/users/1', headers=auth_headers)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        
        response = client.put('/api/users/1', headers=auth_headers)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        
        response = client.delete('/api/users/1', headers=auth_headers)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED 