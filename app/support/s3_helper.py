#Changed Filename to s3_helper.py
from config import Config
from app.support.s3 import S3_Client
from app.support.file_utils import get_unique_file_name

def upload_file_to_s3(file_type, file_name, file_to_upload, user_name):
    s3_folder = get_s3_folder(file_type)
    filename = get_unique_file_name(file_name, user_name)
    filepath = f"{s3_folder}/{filename}"
    return S3_Client().upload_file(filepath, filename, file_to_upload)

def get_object_from_s3(file_type, file_name):
    s3_folder = get_s3_folder(file_type)
    filepath = f"{s3_folder}/{file_name}"
    return S3_Client().get_object(filepath)

def put_object_to_s3(file_type, file_name, file_obj, user_name):
    s3_folder = get_s3_folder(file_type)
    filename = get_unique_file_name(file_name, user_name)
    filepath = f"{s3_folder}/{filename}"
    return S3_Client().put_object(filepath, filename, file_obj)

def generate_presigned_s3_url(file_type, file_name):
    s3_folder = get_s3_folder(file_type)
    filepath = f"{s3_folder}/{file_name}"
    return S3_Client().generate_presigned_url(filepath)

def file_not_found_on_s3(file_type, file_name):
    s3_folder = get_s3_folder(file_type)
    filepath = f"{s3_folder}/{file_name}"
    return S3_Client().file_not_found(filepath)

def get_s3_folder(file_type):
    match file_type:
        case 'user_file':
            return Config.AWS_S3_USER_FILE_FOLDER

