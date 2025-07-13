import pytest
from app.validators.api.schema_validator import SchemaValidator
from app.validators.api.data_validator import DataValidator


@pytest.mark.unit
class TestSchemaValidator:
    """Test cases for SchemaValidator class."""

    def test_valid_user_schema(self):
        """Test validation with valid user data."""
        valid_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'manager'
        }
        
        validator = SchemaValidator(valid_data)
        errors = validator.validate_user_schema()
        
        assert len(errors) == 0

    def test_empty_post_data(self):
        """Test validation with empty post data."""
        validator = SchemaValidator({})
        errors = validator.validate_user_schema()
        
        assert len(errors) == 1
        assert "please provide a valid user schema" in errors[0]

    def test_missing_name(self):
        """Test validation with missing name."""
        invalid_data = {
            'email': 'john@example.com',
            'role': 'manager'
        }
        
        validator = SchemaValidator(invalid_data)
        errors = validator.validate_user_schema()
        
        assert len(errors) == 1
        assert "user name is required" in errors[0]

    def test_empty_name(self):
        """Test validation with empty name."""
        invalid_data = {
            'name': '',
            'email': 'john@example.com',
            'role': 'manager'
        }
        
        validator = SchemaValidator(invalid_data)
        errors = validator.validate_user_schema()
        
        assert len(errors) == 1
        assert "user name is required" in errors[0]

    def test_missing_email(self):
        """Test validation with missing email."""
        invalid_data = {
            'name': 'John Doe',
            'role': 'manager'
        }
        
        validator = SchemaValidator(invalid_data)
        errors = validator.validate_user_schema()
        
        assert len(errors) == 1
        assert "email is required" in errors[0]

    def test_empty_email(self):
        """Test validation with empty email."""
        invalid_data = {
            'name': 'John Doe',
            'email': '',
            'role': 'manager'
        }
        
        validator = SchemaValidator(invalid_data)
        errors = validator.validate_user_schema()
        
        assert len(errors) == 1
        assert "email is required" in errors[0]

    def test_invalid_email_format(self):
        """Test validation with invalid email format."""
        invalid_data = {
            'name': 'John Doe',
            'email': 'invalid-email',
            'role': 'manager'
        }
        
        validator = SchemaValidator(invalid_data)
        errors = validator.validate_user_schema()
        
        assert len(errors) == 1
        assert "invalid email address" in errors[0]

    def test_missing_role(self):
        """Test validation with missing role."""
        invalid_data = {
            'name': 'John Doe',
            'email': 'john@example.com'
        }
        
        validator = SchemaValidator(invalid_data)
        errors = validator.validate_user_schema()
        
        assert len(errors) == 1
        assert "role is required" in errors[0]

    def test_empty_role(self):
        """Test validation with empty role."""
        invalid_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': ''
        }
        
        validator = SchemaValidator(invalid_data)
        errors = validator.validate_user_schema()
        
        assert len(errors) == 1
        assert "role is required" in errors[0]

    def test_invalid_role(self):
        """Test validation with invalid role."""
        invalid_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'invalid_role'
        }
        
        validator = SchemaValidator(invalid_data)
        errors = validator.validate_user_schema()
        
        assert len(errors) == 1
        assert "invalid role" in errors[0]

    def test_valid_agent_role(self):
        """Test validation with valid agent role."""
        valid_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'agent'
        }
        
        validator = SchemaValidator(valid_data)
        errors = validator.validate_user_schema()
        
        assert len(errors) == 0

    def test_valid_manager_role(self):
        """Test validation with valid manager role."""
        valid_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'role': 'manager'
        }
        
        validator = SchemaValidator(valid_data)
        errors = validator.validate_user_schema()
        
        assert len(errors) == 0

    def test_valid_upload_schema(self):
        """Test file upload schema validation with valid data."""
        valid_data = {
            'images': ['image1.jpg', 'image2.png'],
            'documents': ['doc1.pdf']
        }
        
        validator = SchemaValidator(valid_data)
        errors = validator.validate_upload_schema()
        
        assert len(errors) == 0

    def test_empty_upload_schema(self):
        """Test file upload schema validation with empty data."""
        validator = SchemaValidator({})
        errors = validator.validate_upload_schema()
        
        assert len(errors) == 1
        assert "Please use atleast one type to upload files" in errors[0]

    def test_upload_schema_with_empty_files(self):
        """Test file upload schema validation with empty file names."""
        invalid_data = {
            'images': ['image1.jpg', ''],
            'documents': ['']
        }
        
        validator = SchemaValidator(invalid_data)
        errors = validator.validate_upload_schema()
        
        assert len(errors) == 1
        assert "Please select files to upload for" in errors[0]
        assert "images" in errors[0]
        assert "documents" in errors[0]

    def test_schema_validation_exception_handling(self):
        """Test schema validation exception handling."""
        # This will cause an exception due to invalid data structure
        validator = SchemaValidator(None)
        errors = validator.validate_user_schema()
        
        assert len(errors) == 1
        # Should contain the formatted exception message

    def test_upload_schema_exception_handling(self):
        """Test upload schema validation exception handling."""
        # This will cause an exception due to invalid data structure
        validator = SchemaValidator(None)
        errors = validator.validate_upload_schema()
        
        assert len(errors) == 1
        # Should contain the formatted exception message


@pytest.mark.unit
class TestDataValidator:
    """Test cases for DataValidator class."""

    def test_data_validator_initialization(self):
        """Test DataValidator initialization."""
        test_data = {'key': 'value'}
        validator = DataValidator(test_data)
        
        assert validator.post_data == test_data

    def test_data_validator_empty_initialization(self):
        """Test DataValidator initialization with empty data."""
        validator = DataValidator()
        
        assert validator.post_data == {}

    def test_validate_data_returns_empty_errors(self):
        """Test that validate_data returns empty errors list."""
        validator = DataValidator({'test': 'data'})
        errors = validator.validate_data()
        
        assert isinstance(errors, list)
        assert len(errors) == 0

    def test_validate_data_with_different_inputs(self):
        """Test validate_data with various input types."""
        test_cases = [
            {},
            {'name': 'test'},
            {'name': 'test', 'email': 'test@example.com'},
            None,
            []
        ]
        
        for test_data in test_cases:
            validator = DataValidator(test_data)
            errors = validator.validate_data()
            
            assert isinstance(errors, list)
            assert len(errors) == 0  # Currently returns empty list 