from flask import make_response, jsonify
from http import HTTPStatus
from app.validators.api.schema_validator import SchemaValidator   
from app.support.s3_helper import put_object_to_s3
from multiprocessing.pool import ThreadPool
import time
import logging
from werkzeug.datastructures import MultiDict

class FilesUploader(object):

  @classmethod
  def perform(self, request, current_user):
    self.current_user = current_user
    self.file_hash    = {}
    self.file_count   = 0

    self.file_hash, file_list = self.get_filelist(request)

    # validate request body schema
    schema_errors = SchemaValidator(post_data=self.file_hash).validate_upload_schema()
    if len(schema_errors) > 0:
      responseObject = {
          "status": "failed",
          "message": ", ".join(schema_errors)
      }
      return make_response(jsonify(responseObject)), HTTPStatus.UNPROCESSABLE_ENTITY

    start_time = time.time()
    logging.info("uploading files ")
    
    pool  = ThreadPool(processes=len(file_list)*2)
    pool.map(self.upload, file_list)

    end_time = time.time()
    logging.info(f"Time taken for uploading files by {current_user['name']} is: {(end_time - start_time)} s")

    responseObject = {
        "status":"success",
        "message": f"{self.file_count} file{'s'[:self.file_count^1]} uploaded successfully",
        "file_names": self.file_hash
    }

    return make_response(jsonify(responseObject)), HTTPStatus.CREATED

  @classmethod
  def upload(self, file):
    response = put_object_to_s3('user_file', file.filename, file, self.current_user['name'])
    if response is not None:
      self.file_count += 1
      self.replace_file_name(file.filename, response['filename'])

  @classmethod
  def get_filelist(self, request):
    files_hash = MultiDict(request.files).to_dict(flat=False)
    unique_file_list = self.get_unique_files(files_hash)
    nested_files_hash = self.convert_files_hash(files_hash)
    return nested_files_hash, unique_file_list

  @classmethod
  def get_unique_files(self, files_hash):
      unique_files = []
      for key, value in files_hash.items():
          if isinstance(value, list):
            unique_files += [file for file in value if file.filename not in [f.filename for f in unique_files]]
      return unique_files

  @classmethod
  def convert_files_hash(self, files_hash):
      nested_files_hash = {}
      for key, value in files_hash.items():
        if '[' in key:
          nested_key, nested_subkey = key.split('[', 1)
          nested_subkey = nested_subkey[:-1]  # remove closing bracket
          if nested_key not in nested_files_hash:
              nested_files_hash[nested_key] = {}
          nested_files_hash[nested_key][nested_subkey] = [ file.filename for file in value ]
        else:
          nested_files_hash[key] = [ file.filename for file in value ]
      return nested_files_hash

  @classmethod
  def replace_file_name(self, old_file_name, new_file_name):
    for key, value in self.file_hash.items():
        if isinstance(value, list):
            if old_file_name in value:
                value[value.index(old_file_name)] = new_file_name
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if old_file_name in sub_value:
                    sub_value[sub_value.index(old_file_name)] = new_file_name