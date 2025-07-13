import pytest
import tempfile
import os
from app.factory import create_app
from app.models.user import User
from app.models.role import Role
from app.models.feature import Feature
from app.models.feature_role import FeatureRole
from flask import Flask


@pytest.fixture
def app():
    """Create and configure a test Flask app."""
    # Backup original environment variables
    original_env = {}
    test_env_vars = {
        'DATABASE_URI': 'sqlite:///:memory:',
        'SECRET_KEY': 'test-secret-key',
        'CELERY_BROKER_URL': 'memory://',
        'CELERY_RESULT_BACKEND': 'cache+memory://',
        'AWS_ACCESS_KEY': 'test-key',
        'AWS_SECRET_ACCESS_KEY': 'test-secret',
        'AWS_S3_BUCKET': 'test-bucket',
        'AWS_S3_USER_FILE_FOLDER': 'test-folder',
        'SESSION_TIME': '3600',
        'MAIL_SERVER': 'localhost',
        'MAIL_PORT': '1025'
    }
    
    # Set test environment variables
    for key, value in test_env_vars.items():
        original_env[key] = os.environ.get(key)
        os.environ[key] = value
    
    try:
        # Create test configuration
        test_config = {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'WTF_CSRF_ENABLED': False,
            'JWT_SECRET_KEY': 'test-secret-key',
            'SECRET_KEY': 'test-secret-key',
            'SQLALCHEMY_ECHO': False,  # Disable SQL logging in tests
            'SQLALCHEMY_TRACK_MODIFICATIONS': False,
            'CELERY_ALWAYS_EAGER': True,  # Run Celery tasks synchronously
            'CELERY_EAGER_PROPAGATES_EXCEPTIONS': True
        }
        
        # Create the app with test configuration override
        app = create_app(config_override=test_config)
        
        with app.app_context():
            from app.factory import db
            
            # Drop all tables if they exist (clean slate)
            db.drop_all()
            
            # Create all tables
            db.create_all()
            
            # Create test data
            _create_test_data()
            
            yield app
            
            # Clean up
            db.session.remove()
            db.drop_all()
            
    finally:
        # Restore original environment variables
        for key, original_value in original_env.items():
            if original_value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = original_value


@pytest.fixture
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test runner for the Flask app."""
    return app.test_cli_runner()


@pytest.fixture
def auth_headers(client):
    """Get authentication headers for API requests."""
    # Create a test user and get token
    login_data = {
        'email': 'admin@test.com'
    }
    
    response = client.post('/api/token', json=login_data)
    token = response.get_json()['token']
    
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        'name': 'Test User',
        'email': 'test@example.com',
        'role': 'manager'
    }


@pytest.fixture
def sample_user_credentials():
    """Sample user credentials for authentication."""
    return {
        'email': 'admin@test.com',
        'password': 'password123'
    }


def _create_test_data():
    """Create test data for the database."""
    from app.factory import db
    
    # Check if data already exists to avoid duplicates
    if Role.query.count() > 0:
        return
    
    try:
        # Create roles
        admin_role = Role(name='admin')
        manager_role = Role(name='manager')
        agent_role = Role(name='agent')
        
        db.session.add(admin_role)
        db.session.add(manager_role)
        db.session.add(agent_role)
        db.session.commit()
        
        # Create features
        user_feature = Feature(name='user_resource')
        file_feature = Feature(name='file_resource')
        
        db.session.add(user_feature)
        db.session.add(file_feature)
        db.session.commit()
        
        # Create feature-role associations
        admin_user_access = FeatureRole(feature_id=user_feature.id, role_id=admin_role.id)
        admin_file_access = FeatureRole(feature_id=file_feature.id, role_id=admin_role.id)
        
        db.session.add(admin_user_access)
        db.session.add(admin_file_access)
        db.session.commit()
        
        # Create test users
        admin_user = User(
            name='Admin User',
            email='admin@test.com',
            role_id=admin_role.id
        )
        
        test_user = User(
            name='Test User',
            email='test@test.com',
            role_id=manager_role.id
        )
        
        db.session.add(admin_user)
        db.session.add(test_user)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        # If there's an error, try to continue without test data
        print(f"Warning: Could not create test data: {e}")


@pytest.fixture
def mock_s3():
    """Mock S3 operations for testing."""
    import unittest.mock as mock
    
    with mock.patch('app.support.s3_helper.put_object_to_s3') as mock_put:
        mock_put.return_value = True
        with mock.patch('app.support.s3_helper.generate_presigned_s3_url') as mock_presigned:
            mock_presigned.return_value = 'https://mock-presigned-url.com'
            yield {
                'put_object': mock_put,
                'presigned_url': mock_presigned
            }


@pytest.fixture
def mock_celery():
    """Mock Celery tasks for testing."""
    import unittest.mock as mock
    
    with mock.patch('app.workers.user_worker.user_email_worker.delay') as mock_delay:
        mock_delay.return_value.task_id = 'test-task-id'
        yield mock_delay 