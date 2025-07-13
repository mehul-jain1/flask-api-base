import datetime
import os

from dotenv import dotenv_values

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # env values
    env_config = dotenv_values(".env")

    # Secret key
    SECRET_KEY = os.environ.get("SECRET_KEY") or env_config["SECRET_KEY"]
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(
        days=365, hours=0, minutes=0, seconds=0
    )

    # Enable debug mode.
    DEBUG = True

    # max file upload size set to 2000 MiB
    MAX_CONTENT_LENGTH = 2000 * 1000 * 1000

    # Connect to the database
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URI") or env_config["DATABASE_URI"]
    )
    SQLALCHEMY_ECHO = True
    # Turn off the Flask-SQLAlchemy event system and warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY") or env_config["AWS_ACCESS_KEY"]
    AWS_SECRET_ACCESS_KEY = (
        os.environ.get("AWS_SECRET_ACCESS_KEY") or env_config["AWS_SECRET_ACCESS_KEY"]
    )
    AWS_S3_BUCKET = os.environ.get("AWS_S3_BUCKET") or env_config["AWS_S3_BUCKET"]
    AWS_S3_USER_FILE_FOLDER = (
        os.environ.get("AWS_S3_USER_FILE_FOLDER")
        or env_config["AWS_S3_USER_FILE_FOLDER"]
    )
    CELERY_BROKER_URL = (
        os.environ.get("CELERY_BROKER_URL") or env_config["CELERY_BROKER_URL"]
    )
    CELERY_RESULT_BACKEND = (
        os.environ.get("CELERY_RESULT_BACKEND") or env_config["CELERY_RESULT_BACKEND"]
    )
    SESSION_TIME = os.environ.get("SESSION_TIME") or env_config["SESSION_TIME"]
    task_acks_late = True

    # Flask-Mail configuration
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "mailhog")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 1025))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "false").lower() in ("true", "1", "t")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
