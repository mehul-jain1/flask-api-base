import pytest
import json
from unittest.mock import patch, MagicMock
from http import HTTPStatus
from werkzeug.exceptions import RequestEntityTooLarge
from io import BytesIO


@pytest.mark.api
@pytest.mark.auth
class TestFilesController:
    """Test cases for files controller endpoints."""

    def test_upload_file_success(self, client, auth_headers, mock_s3):
        """Test successful file upload."""
        with patch('app.support.files_uploader.FilesUploader.perform') as mock_perform:
            mock_response = MagicMock()
            mock_response.status_code = HTTPStatus.OK
            mock_response.get_json.return_value = {
                'status': 'success',
                'message': 'File uploaded successfully'
            }
            mock_perform.return_value = mock_response
            
            # Create a test file
            data = {
                'file': (BytesIO(b'test file content'), 'test.txt')
            }
            
            response = client.post('/api/files/upload-files', 
                                 data=data, 
                                 headers=auth_headers,
                                 content_type='multipart/form-data')
            
            assert response.status_code == HTTPStatus.OK
            mock_perform.assert_called_once()

    def test_upload_file_too_large(self, client, auth_headers):
        """Test file upload with entity too large error."""
        with patch('app.support.files_uploader.FilesUploader.perform') as mock_perform:
            mock_perform.side_effect = RequestEntityTooLarge()
            
            data = {
                'file': (BytesIO(b'large file content'), 'large.txt')
            }
            
            response = client.post('/api/files/upload-files', 
                                 data=data, 
                                 headers=auth_headers,
                                 content_type='multipart/form-data')
            
            data = response.get_json()
            
            assert response.status_code == HTTPStatus.REQUEST_ENTITY_TOO_LARGE
            assert data['status'] == 'failed'
            assert 'Please upload files less then 2000 Mib' in data['message']

    def test_upload_file_unauthorized(self, client):
        """Test file upload without authentication."""
        data = {
            'file': (BytesIO(b'test file content'), 'test.txt')
        }
        
        response = client.post('/api/files/upload-files', 
                             data=data,
                             content_type='multipart/form-data')
        
        assert response.status_code in [HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN]

    def test_upload_file_general_error(self, client, auth_headers):
        """Test file upload with general error."""
        with patch('app.support.files_uploader.FilesUploader.perform') as mock_perform:
            mock_perform.side_effect = Exception("Upload failed")
            
            data = {
                'file': (BytesIO(b'test file content'), 'test.txt')
            }
            
            response = client.post('/api/files/upload-files', 
                                 data=data, 
                                 headers=auth_headers,
                                 content_type='multipart/form-data')
            
            # Should return 500 for unhandled exceptions
            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR

    def test_get_presigned_url_success(self, client, auth_headers, mock_s3):
        """Test successful presigned URL generation."""
        with patch('app.controllers.api.v1.files_controller.generate_presigned_s3_url') as mock_generate:
            mock_generate.return_value = "https://test-presigned-url.com"
            
            response = client.get('/api/files/presigned_url?file_type=user_file&file_name=test.jpg',
                                headers=auth_headers)

            assert response.status_code == HTTPStatus.OK
            # The mock should return the mocked presigned URL
            mock_generate.assert_called_once_with('user_file', 'test.jpg')

    def test_get_presigned_url_missing_params(self, client, auth_headers):
        """Test presigned URL generation with missing parameters."""
        # Missing file_type
        response = client.get('/api/files/presigned_url?file_name=test.jpg', 
                            headers=auth_headers)
        
        # Should still call the function, but with None values
        assert response.status_code == HTTPStatus.OK
        
        # Missing file_name
        response = client.get('/api/files/presigned_url?file_type=image', 
                            headers=auth_headers)
        
        assert response.status_code == HTTPStatus.OK

    def test_get_presigned_url_unauthorized(self, client):
        """Test presigned URL generation without authentication."""
        response = client.get('/api/files/presigned_url?file_type=image&file_name=test.jpg')
        
        assert response.status_code in [HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN]

    def test_get_presigned_url_no_params(self, client, auth_headers, mock_s3):
        """Test presigned URL generation without any parameters."""
        with patch('app.controllers.api.v1.files_controller.generate_presigned_s3_url') as mock_generate:
            mock_generate.return_value = "https://test-presigned-url.com"
            
            response = client.get('/api/files/presigned_url', headers=auth_headers)

            assert response.status_code == HTTPStatus.OK
            # Should be called with None values
            mock_generate.assert_called_once_with(None, None)

    @patch('app.controllers.api.v1.files_controller.generate_presigned_s3_url')
    def test_get_presigned_url_s3_error(self, mock_generate, client, auth_headers):
        """Test presigned URL generation with S3 error."""
        mock_generate.side_effect = Exception("S3 Error")

        response = client.get('/api/files/presigned_url?file_type=user_file&file_name=test.jpg',
                            headers=auth_headers)

        # Should return 500 for unhandled exceptions
        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.json['status'] == 'failed'
        assert 'S3 Error' in response.json['message']

    def test_upload_files_endpoint_methods(self, client, auth_headers):
        """Test allowed methods for upload files endpoint."""
        # Test unsupported methods
        response = client.get('/api/files/upload-files', headers=auth_headers)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        
        response = client.put('/api/files/upload-files', headers=auth_headers)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        
        response = client.delete('/api/files/upload-files', headers=auth_headers)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_presigned_url_endpoint_methods(self, client, auth_headers):
        """Test allowed methods for presigned URL endpoint."""
        # Test unsupported methods
        response = client.post('/api/files/presigned_url', headers=auth_headers)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        
        response = client.put('/api/files/presigned_url', headers=auth_headers)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED
        
        response = client.delete('/api/files/presigned_url', headers=auth_headers)
        assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED

    def test_upload_multiple_files(self, client, auth_headers):
        """Test uploading multiple files."""
        with patch('app.support.files_uploader.FilesUploader.perform') as mock_perform:
            mock_response = MagicMock()
            mock_response.status_code = HTTPStatus.OK
            mock_response.get_json.return_value = {
                'status': 'success',
                'message': 'Files uploaded successfully'
            }
            mock_perform.return_value = mock_response
            
            # Create multiple test files
            data = {
                'files': [
                    (BytesIO(b'test file 1'), 'test1.txt'),
                    (BytesIO(b'test file 2'), 'test2.txt')
                ]
            }
            
            response = client.post('/api/files/upload-files', 
                                 data=data, 
                                 headers=auth_headers,
                                 content_type='multipart/form-data')
            
            assert response.status_code == HTTPStatus.OK
            mock_perform.assert_called_once()

    def test_upload_empty_file(self, client, auth_headers):
        """Test uploading empty file."""
        with patch('app.support.files_uploader.FilesUploader.perform') as mock_perform:
            mock_perform.side_effect = Exception("Empty file not allowed")

            data = {
                'file': (BytesIO(b''), 'empty.txt')
            }

            response = client.post('/api/files/upload-files',
                                 data=data,
                                 headers=auth_headers,
                                 content_type='multipart/form-data')

            assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
            assert response.json['status'] == 'failed'
            assert 'Empty file not allowed' in response.json['message'] 