from app.models.user import User
from flask import request, make_response, jsonify
from app.api_routes import api_bp
from http import HTTPStatus
from app.support.auth_helper import encode_jwt_token


@api_bp.route('/token', methods=['POST'])
def getTokenAPI():
    try:
        post_data = request.get_json()
        
        # Check if email is provided
        if not post_data or 'email' not in post_data:
            responseObject = {
                "status": "failed",
                "message": "email is required"
            }
            return make_response(jsonify(responseObject)), HTTPStatus.BAD_REQUEST
            
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
                    return make_response(jsonify(responseObject)), HTTPStatus.BAD_REQUEST
            except Exception as e:
                responseObject = {
                    "status": "failed",
                    "message": format(e)
                }
                return make_response(jsonify(responseObject)), HTTPStatus.BAD_REQUEST
    except Exception as e:
        responseObject = {
            "status": "failed",
            "message": format(e)
        }
        return make_response(jsonify(responseObject)), HTTPStatus.BAD_REQUEST 