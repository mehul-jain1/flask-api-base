from flask import request, make_response, jsonify
from app.api_routes import api_bp
from http import HTTPStatus
from app.support.auth_helper import api_token_required
from app.support.files_uploader import FilesUploader
from app.support.s3_helper import generate_presigned_s3_url
from werkzeug.exceptions import RequestEntityTooLarge


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
    except Exception as e:
        responseObject = {
            "status": "failed", 
            "message": str(e)
        }
        return make_response(jsonify(responseObject)), HTTPStatus.INTERNAL_SERVER_ERROR


@api_bp.route('/files/presigned_url', methods=['GET'])
@api_token_required('user_resource')
def getPresignedUrl(current_user):
    try:
        file_type = request.args.get('file_type')
        file_name = request.args.get('file_name')
        return generate_presigned_s3_url(file_type, file_name)
    except Exception as e:
        responseObject = {
            "status": "failed", 
            "message": str(e)
        }
        return make_response(jsonify(responseObject)), HTTPStatus.INTERNAL_SERVER_ERROR 