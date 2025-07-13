import logging

import boto3

from config import Config

AWS_ACCESS_KEY = Config.AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = Config.AWS_SECRET_ACCESS_KEY
S3_BUCKET = Config.AWS_S3_BUCKET


class S3_Client(object):
    def __init__(self):
        # creating session with boto3
        self.session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        # creating S3 client from the session
        self.s3_client = self.session.client("s3")

        # creating S3 resource from the session
        self.s3_resource = self.session.resource("s3")

    def upload_file(self, filepath, filename, file_to_upload):
        try:
            # uploading file to S3 bucket
            self.s3_resource.Bucket(S3_BUCKET).upload_file(file_to_upload, filepath)
        except Exception as e:
            logging.error(e)
            return None

        return {"filename": filename}

    def get_object(self, filepath):
        try:
            # getting file object from s3 bucket
            response = self.s3_client.get_object(Bucket=S3_BUCKET, Key=filepath)
            self.s3_client.head_object(Bucket=S3_BUCKET, Key=filepath)
        except Exception as e:
            logging.error(e)
            return None

        return response

    def put_object(self, filepath, filename, file_obj):
        try:
            response = self.s3_client.put_object(
                Bucket=S3_BUCKET, Key=filepath, Body=file_obj
            )
        except Exception as e:
            logging.error(e)
            return None

        return {
            "status": response["ResponseMetadata"]["HTTPStatusCode"],
            "filename": filename,
        }

    def generate_presigned_url(self, filepath, expiration=3600):
        try:
            response = self.s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": S3_BUCKET,
                    "Key": filepath,
                    "ResponseContentDisposition": "attachment",
                },
                ExpiresIn=expiration,
            )
        except Exception as e:
            logging.error(e)
            return None

        return response

    def file_not_found(self, filepath):
        try:
            self.s3_client.head_object(Bucket=S3_BUCKET, Key=filepath)
        except Exception as e:
            logging.error(e)
            return True

        return False
