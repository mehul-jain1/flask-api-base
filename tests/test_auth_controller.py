import pytest
import json
from unittest.mock import patch
from http import HTTPStatus


@pytest.mark.api
@pytest.mark.auth
class TestAuthController:
    """Test cases for authentication controller endpoints."""

    def test_get_token_success(self, client, sample_user_credentials):
        """Test successful token generation."""
        # Use existing test user from conftest
        login_data = {
            'email': 'admin@test.com'
        }
        
        response = client.post('/api/token', json=login_data)
        data = response.get_json()
        
        assert response.status_code == HTTPStatus.ACCEPTED
        assert data['status'] == 'success'
        assert 'token' in data
        assert data['token'] is not None

    def test_get_token_user_not_found(self, client):
        """Test token generation with non-existent user."""
        login_data = {
            'email': 'nonexistent@test.com'
        }
        
        response = client.post('/api/token', json=login_data)
        data = response.get_json()
        
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert data['status'] == 'failed'
        assert data['message'] == 'user not found'

    def test_get_token_missing_email(self, client):
        """Test token generation without email."""
        login_data = {}
        
        response = client.post('/api/token', json=login_data)
        data = response.get_json()
        
        # This should trigger a KeyError which gets handled as BAD_REQUEST
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert data['status'] == 'failed'

    def test_get_token_invalid_json(self, client):
        """Test token generation with invalid JSON."""
        response = client.post('/api/token', data='invalid json')
        
        assert response.status_code == HTTPStatus.BAD_REQUEST

    @patch('app.controllers.api.v1.auth_controller.encode_jwt_token')
    def test_get_token_encoding_failure(self, mock_encode, client):
        """Test token generation when encoding fails."""
        mock_encode.return_value = None
        
        login_data = {
            'email': 'admin@test.com'
        }
        
        response = client.post('/api/token', json=login_data)
        
        data = response.get_json()
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert data['status'] == 'failed'
        assert data['message'] == 'token generation failed'

    @patch('app.controllers.api.v1.auth_controller.encode_jwt_token')
    def test_get_token_encoding_exception(self, mock_encode, client):
        """Test token generation when encoding raises an exception."""
        mock_encode.side_effect = Exception("Encoding error")
        
        login_data = {
            'email': 'admin@test.com'
        }
        
        response = client.post('/api/token', json=login_data)
        data = response.get_json()
        
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert data['status'] == 'failed'
        assert 'Encoding error' in data['message']

    def test_get_token_endpoint_methods(self, client):
        """Test that the token endpoint only accepts POST requests."""
        # Test GET request
        response = client.get('/api/token')
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        
        # Test PUT request
        response = client.put('/api/token')
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        
        # Test DELETE request
        response = client.delete('/api/token')
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED 