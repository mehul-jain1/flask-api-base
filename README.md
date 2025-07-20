# Flask API Base

[![Python Tests](https://github.com/mehul-jain1/flask-api-base/actions/workflows/pytest.yml/badge.svg)](https://github.com/mehul-jain1/flask-api-base/actions/workflows/pytest.yml)
[![Code Quality Check](https://github.com/mehul-jain1/flask-api-base/actions/workflows/check_and_validate.yml/badge.svg)](https://github.com/mehul-jain1/flask-api-base/actions/workflows/check_and_validate.yml)

A feature-rich boilerplate for building RESTful APIs using Flask. This project provides a solid foundation with a modular structure, ready for extension and customization.

## Architecture

![Flask API Base Architecture](compose/local/flask/api-base-arch.png)

## Features

- **Authentication**: JWT-based token authentication.
- **Async Tasks**: Celery with Redis for background task processing.
- **Database**: Flask-SQLAlchemy and Flask-Migrate for database operations.
- **File Storage**: S3 integration for file uploads.
- **Email**: Flask-Mail integration, with MailHog for local development.
- **Containerization**: Fully containerized with Docker and Docker Compose.
- **API Documentation**: Swagger UI for interactive API documentation.
- **Configuration**: Environment-based configuration management.

## Project Structure

```
flask-api-base/
├── app/                  # Main application module
│   ├── api_routes.py     # API blueprint and route registration
│   ├── controllers/      # API controllers organized by version
│   │   └── api/
│   │       └── v1/       # Version 1 controllers
│   │           ├── auth_controller.py
│   │           ├── users_controller.py
│   │           └── files_controller.py
│   ├── models/           # SQLAlchemy models
│   ├── services/         # Business logic
│   ├── support/          # Helper modules (auth, S3, etc.)
│   ├── validators/       # Input validation classes
│   │   └── api/
│   │       ├── data_validator.py
│   │       └── schema_validator.py
│   └── workers/          # Celery worker definitions
├── compose/              # Docker-compose configurations
├── migrations/           # Database migration scripts
├── tests/                # Test suite
└── ...
```

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed on your local machine.

### Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd flask-api-base
    ```

2.  **Environment Variables:**
    Create a `.env` file in the `.envdir` directory by copying the example.
    ```bash
    cp .env.example .envdir/.env
    ```
    Update `.envdir/.env` with your specific configurations (e.g., AWS credentials, secret key).

### Running the Application

1.  **Build and start the services:**
    ```bash
    docker-compose build
    docker-compose up
    ```

2.  **Access the application:**
    Once the containers are running, the following services will be available:
    - **API**: `http://localhost:9000/api`
    - **Swagger Docs**: `http://localhost:9000/api/docs`
    - **MailHog**: `http://localhost:8025`
    - **Flower (Celery Monitor)**: `http://localhost:5557`

3.  **Stopping the application:**
    To stop the running containers, press `Ctrl+C` in the terminal where `docker-compose up` is running.

## Database Migrations

To apply database migrations, first shell into the `web` container:
```bash
docker-compose exec web /bin/bash
```
Then, run the migration commands:
```bash
flask db migrate -m "Initial migration"
flask db upgrade
```

## Seeding Data

The project includes a seeder to populate the database with initial data.
```bash
docker-compose exec web /bin/bash
flask seed run
```

## Configuration

- Application configs are stored at `.envdir/.env`
- Updated the `GUNICORN_CMD_ARGS="--bind 0.0.0.0:9000 --workers=2 --threads=4 --worker-class=gthread --worker-tmp-dir /dev/shm"` for CMD line in Docker file.

## Pipeline Setup

The project includes GitHub Actions workflows for continuous integration:
- **pytest.yml**: Runs the test suite
- **check_and_validate.yml**: Code quality checks

## Docker Setup

1. Install Docker Desktop
2. Navigate to the root of the directory in terminal. You should be at the same level as the `docker-compose.yml` file.
3. Run `docker-compose build`
4. The step above will take around 5-10 minutes for the first time as the images get downloaded. Subsequent executions will be faster.
5. If the above step runs to its end successfully, run `docker image ls`. You should see below images:
   - `flask_api_base_celery_worker`
   - `flask_api_base_webapp`
   - `flask_api_base_celery_flower`
   - `redis`
6. Run `docker-compose up`
7. If the above runs successfully, the application can be browsed at `http://localhost:9000`
8. If you wish to stop the container, press `ctrl+c` in the terminal

## API Documentation

The API documentation is available via Swagger UI at `http://localhost:9000/api/docs` when the application is running.

## Testing

Run the test suite using:
```bash
docker-compose exec web python -m pytest
```

Or run tests with coverage:
```bash
docker-compose exec web python -m pytest --cov=app
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Additional Resources

For a comprehensive comparison between SQLAlchemy and ActiveRecord patterns, see [SQLALCHEMY_VS_ACTIVERECORD_GUIDE.md](SQLALCHEMY_VS_ACTIVERECORD_GUIDE.md). 