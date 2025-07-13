# Test Suite Documentation

This directory contains comprehensive tests for the Flask API Base project using pytest.

## Quick Start

### Running Tests (Recommended)
```bash
# Run all tests with warnings suppressed (clean output)
./run_tests.sh

# Run specific test file
./run_tests.sh tests/test_auth_controller.py

# Run specific test with verbose output
./run_tests.sh tests/test_auth_controller.py::TestAuthController::test_get_token_success -v
```

### Alternative Methods
```bash
# Run with manual warning suppression
PYTHONWARNINGS=ignore python -m pytest tests/ -v

# Run with warnings visible (not recommended for clean output)
python -m pytest tests/ -v
```

## Test Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── pytest.ini              # Pytest settings and markers
├── test_auth_controller.py  # Authentication controller tests
├── test_users_controller.py # Users controller tests
├── test_files_controller.py # Files controller tests
├── test_validators.py       # Validator classes tests
├── locust.py               # Load testing with Locust
└── fixtures/               # Test fixtures and sample data
```

## Test Categories

### 🔐 Authentication Tests (`test_auth_controller.py`)
- Token generation success/failure scenarios
- User authentication validation
- Error handling for invalid credentials
- JWT token encoding/decoding

### 👥 Users Tests (`test_users_controller.py`)
- User CRUD operations (Create, Read, Update, Delete)
- User input validation
- Pagination testing
- Authorization checks
- Error handling for various scenarios

### 📁 Files Tests (`test_files_controller.py`)
- File upload functionality
- S3 presigned URL generation
- File size validation
- Error handling for upload failures
- Multiple file uploads

### ✅ Validators Tests (`test_validators.py`)
- Schema validation for user data
- Data validation logic
- Email format validation
- Role validation
- File upload schema validation

## Running Tests

### Prerequisites
Make sure you have pytest installed (already in requirements.txt):
```bash
pip install pytest pytest-xdist
```

### Basic Test Commands

**Run all tests:**
```bash
pytest
```

**Run with verbose output:**
```bash
pytest -v
```

**Run specific test file:**
```bash
pytest tests/test_auth_controller.py
```

**Run specific test class:**
```bash
pytest tests/test_users_controller.py::TestUsersController
```

**Run specific test method:**
```bash
pytest tests/test_auth_controller.py::TestAuthController::test_get_token_success
```

### Test Markers

The tests use custom markers to categorize different types of tests:

**Run only API tests:**
```bash
pytest -m api
```

**Run only unit tests:**
```bash
pytest -m unit
```

**Run only authentication tests:**
```bash
pytest -m auth
```

**Run tests in parallel (faster):**
```bash
pytest -n auto
```

**Exclude slow tests:**
```bash
pytest -m "not slow"
```

### Test Coverage

**Run tests with coverage report:**
```bash
pytest --cov=app --cov-report=html
```

**Generate coverage report:**
```bash
pytest --cov=app --cov-report=term-missing
```

## Test Configuration

### Environment Variables
Tests use a separate testing configuration. Key settings:
- `TESTING=True`
- SQLite in-memory database
- JWT secret key for testing
- Disabled CSRF protection

### Fixtures (`conftest.py`)

**Core Fixtures:**
- `app`: Flask application instance for testing
- `client`: Test client for making HTTP requests
- `auth_headers`: Pre-authenticated headers for API requests
- `sample_user_data`: Sample user data for testing

**Mock Fixtures:**
- `mock_s3`: Mocked S3 operations
- `mock_celery`: Mocked Celery tasks

### Test Database
Tests use a temporary SQLite database that is:
- Created fresh for each test session
- Populated with test data (users, roles, features)
- Cleaned up after tests complete

## Writing New Tests

### Test Structure
Follow this pattern for new tests:

```python
import pytest
from http import HTTPStatus

@pytest.mark.api
class TestNewController:
    """Test cases for new controller."""
    
    def test_endpoint_success(self, client, auth_headers):
        """Test successful endpoint call."""
        response = client.get('/api/endpoint', headers=auth_headers)
        
        assert response.status_code == HTTPStatus.OK
        assert response.get_json()['status'] == 'success'
    
    def test_endpoint_unauthorized(self, client):
        """Test endpoint without authentication."""
        response = client.get('/api/endpoint')
        
        assert response.status_code == HTTPStatus.UNAUTHORIZED
```

### Best Practices

1. **Use descriptive test names** - Test name should explain what it's testing
2. **One assertion per test** - Keep tests focused and simple
3. **Use fixtures** - Leverage existing fixtures for common setup
4. **Test edge cases** - Include error scenarios and boundary conditions
5. **Mock external dependencies** - Mock S3, Celery, external APIs
6. **Use appropriate markers** - Mark tests with `@pytest.mark.api`, `@pytest.mark.unit`, etc.

### Mocking Examples

**Mock S3 operations:**
```python
def test_with_s3_mock(self, client, auth_headers, mock_s3):
    # S3 operations are automatically mocked
    response = client.post('/api/files/upload', data=file_data, headers=auth_headers)
    mock_s3['put_object'].assert_called_once()
```

**Mock Celery tasks:**
```python
def test_with_celery_mock(self, client, auth_headers, mock_celery):
    response = client.post('/api/users', json=user_data, headers=auth_headers)
    mock_celery.assert_called_once()
```

## Continuous Integration

Tests are designed to run in CI/CD pipelines:

**GitHub Actions example:**
```yaml
- name: Run tests
  run: |
    pytest --cov=app --cov-report=xml
    
- name: Upload coverage
  uses: codecov/codecov-action@v1
```

## Load Testing

Use Locust for load testing:
```bash
locust --host=http://localhost:9000/ -f tests/locust.py --headless -u 100 -r 10 --run-time 15m
```

## Debugging Tests

**Run tests with debugging:**
```bash
pytest -s -vv tests/test_auth_controller.py::TestAuthController::test_get_token_success
```

**Drop into debugger on failure:**
```bash
pytest --pdb
```

**See print statements:**
```bash
pytest -s
```

## Common Issues

1. **Database conflicts** - Tests use isolated database per session
2. **Authentication issues** - Use `auth_headers` fixture for authenticated requests
3. **Mocking problems** - Ensure mocks are applied to the correct import paths
4. **Async issues** - Celery tasks are mocked to avoid async complications

## Test Data

Test data is automatically created in `conftest.py`:
- Admin user: `admin@test.com`
- Test user: `test@test.com`
- Roles: admin, manager, agent
- Features: user_resource, file_resource

This ensures consistent test data across all test runs. 