from app.models.user import User
from flask import request, make_response, jsonify, session
from app.api import api_bp
from http import HTTPStatus
from .schema_validator import SchemaValidator
from .data_validator import DataValidator
from app.support.auth_helper import api_token_required, encode_jwt_token, validate_user_permission
from app.workers.user_worker import user_email_worker
from app.support.files_uploader import FilesUploader
from app.support.s3_helper import generate_presigned_s3_url
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.exceptions import NotFound
from app import celery
from flask import Response
import pdb
from app.services.users.saver import UserSaver

@api_bp.route('/token', methods=['POST'])
def getTokenAPI():
    post_data = request.get_json()
    user = User.query.filter_by(email=post_data['email']).first()
    if not user:
        responseObject = {
            "status": "failed",
            "message": "user not found"
        }
        return make_response(jsonify(responseObject)), HTTPStatus.NOT_FOUND
    else:
        try:
            token = encode_jwt_token(user)
            if token:
                responseObject = {
                    "status": "success",
                    "token": token
                }
                return make_response(jsonify(responseObject)), HTTPStatus.ACCEPTED
            else:
                responseObject = {
                    "status": "failed",
                    "message": "token generation failed"
                }
                return make_response(jsonify(responseObject)), HTTPStatus.NO_CONTENT
        except Exception as e:
            responseObject = {
                "status": "failed",
                "message": format(e)
            }
            return make_response(jsonify(responseObject)), HTTPStatus.BAD_REQUEST
@api_bp.route('/users', methods=['POST'])
@api_token_required('user_resource')
def postUserAPI(current_user):
    post_data = request.get_json()

    # validate request body schema 
    schema_errors = SchemaValidator(post_data=post_data).validate_user_schema()
    if len(schema_errors) > 0:
        responseObject =  {
            "status": "failed",
            "message": ", ".join(schema_errors)
        }
        return make_response(jsonify(responseObject)), HTTPStatus.BAD_REQUEST

    # validate request body data
    data_errors = DataValidator(post_data=post_data).validate_data()
    if len(data_errors) > 0:
        responseObject =  {
            "status": "errors",
            "message": ", ".join(data_errors)
        }

        return make_response(jsonify(responseObject)), HTTPStatus.BAD_REQUEST
         
    user_saver = UserSaver(post_data)
    user = user_saver.save()
    if user is not None:
        async_result = user_email_worker.delay(user.id)
        responseObject = { 
            'status': 'success',
            'message': 'User created successfully, they will receive an email with their credentials',
            'user': user.serialize,
            'job_result': {
                'job_id': async_result.task_id,
            }
        }

        return make_response(jsonify(responseObject)), HTTPStatus.CREATED
    
    else:
        responseObject = {
            'status': 'failed',
            'message': 'User creation failed',
            'errors': user_saver.errors
        }
        return make_response(jsonify(responseObject)), HTTPStatus.BAD_REQUEST

@api_bp.route('/users', methods=['GET'])
@api_token_required('user_resource')
def getAllUsersAPI(current_user):
    try:
        records = User.query.order_by(User.id.desc())

        if records:
            # default page = 1
            page_number = int(request.args.get('pageNumber', 1))

            # default per_page = 10
            page_size = int(request.args.get('pageSize', 10))
            
            # query - default descending order
            users = records.paginate(page=page_number, per_page=page_size)
            responseObject = {
                "status": "success",
                "message": f"{len(users.items)} users fetched",
                "users": [ u.serialize for u in users.items ],
                "pagination": {
                    "total": users.total,
                    "page": page_number,
                    "per_page": page_size,
                    "pages": users.pages,
                }
            }
            return make_response(jsonify(responseObject)), HTTPStatus.ACCEPTED
        else:
            responseObject = {
                "status": "failed",
                "message": "user query failed"
            }
            return make_response(jsonify(responseObject)), HTTPStatus.NO_CONTENT
    except NotFound:
        responseObject = {
            "status": "failed",
            "message": "error fetching users",
            "pagination": {
                "page": page_number,
                "per_page": page_size,
            }
        }
        return make_response(jsonify(responseObject)), HTTPStatus.NOT_FOUND

@api_bp.route('/users/<id>', methods=['GET'])
@api_token_required('user_resource')
def getUserAPI(current_user, id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            responseObject = {
                "status": "success",
                "message": "user record fetched",
                "user": user.serialize
            }
            return make_response(jsonify(responseObject)), HTTPStatus.OK
        else:
            raise(UnboundLocalError)
    except UnboundLocalError:
        responseObject = {
            "status": "failed",
            "message": "User record not found"
        }
        return make_response(jsonify(responseObject)), HTTPStatus.NOT_FOUND
    except Exception as e:
        responseObject = {
            "status": "failed",
            "message": format(e)
        }
        return make_response(jsonify(responseObject)), HTTPStatus.BAD_REQUEST

@api_bp.route('/files/upload-files', methods=['POST'])
@api_token_required('user_resource')
def uploadAPI(current_user):
  try:
    response = FilesUploader.perform(request, current_user)
    return response
  except RequestEntityTooLarge as e:
    responseObject = {
        "status": "failed", 
        "message": "Please upload files less then 2000 Mib"
    }
    return make_response(jsonify(responseObject)), HTTPStatus.REQUEST_ENTITY_TOO_LARGE


@api_bp.route('/files/presigned_url', methods=['GET'])
@api_token_required('user_resource')
def getPresignedUrl(current_user):
  file_type = request.args.get('file_type')
  file_name = request.args.get('file_name')
  return generate_presigned_s3_url(file_type, file_name)
