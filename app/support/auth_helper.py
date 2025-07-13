import datetime
import time
from datetime import timezone
from functools import wraps
from http import HTTPStatus

import jwt
from flask import jsonify, make_response, render_template, request, session

from app import Config
from app.models.feature import Feature
from app.models.feature_role import FeatureRole
from app.models.role import Role
from app.models.user import User


# decorator for verifying the JWT for UI routes
# web token authentication
def web_token_required(allowed_feature):
    def decorator(view_func):
        @wraps(view_func)
        def decorated(*args, **kwargs):
            current_user = None
            error_msg = None
            token = None

            # using session variables
            if session and session.get("token"):
                token = session.get("token")
            else:
                token = get_jwt_token(request)

            if token:
                try:
                    # Getting user info from JWT token
                    current_user = get_user_info(token)
                    if current_user:
                        valid_access = validate_user_permission(
                            allowed_feature, current_user["role"]
                        )
                        if not valid_access:
                            error_msg = "User does not have sufficient permission to view this page. Please contact your administrator!"
                        else:
                            session["token"] = encode_jwt_token(current_user)
                            session["expire_at"] = int(time.time()) + int(
                                Config.SESSION_TIME
                            )

                    else:
                        error_msg = "User is inactive or does not exit. Please contact your administrator!"

                except Exception:
                    error_msg = (
                        "Something went wrong. Please contact your administrator!"
                    )

            else:
                error_msg = (
                    "Session timeout. Please visit application to connect to tool!"
                )

            # checking errors
            if error_msg:
                return render_template(
                    "web/login.html", title="Api Base Tool", message=error_msg
                )

            return view_func(current_user, *args, **kwargs)

        return decorated

    return decorator


# decorator for verifying the JWT for API endpoints
def api_token_required(allowed_feature):
    def decorator(view_func):
        @wraps(view_func)
        def decorated(*args, **kwargs):
            token = get_jwt_token(request)

            if not token:
                responseObject = {"status": "failed", "message": "token is missing"}
                return make_response(jsonify(responseObject)), HTTPStatus.UNAUTHORIZED

            try:
                # Getting user info from JWT token
                current_user = get_user_info(token)
                if not current_user:
                    responseObject = {
                        "status": "failed",
                        "message": "User is inactive or does not exit. Please contact your administrator!",
                    }
                    return (
                        make_response(jsonify(responseObject)),
                        HTTPStatus.UNAUTHORIZED,
                    )

                valid_access = validate_user_permission(
                    allowed_feature, current_user["role"]
                )
                if not valid_access:
                    responseObject = {
                        "status": "failed",
                        "message": "User does not have sufficient permission to make this request. Please contact your administrator!",
                    }
                    return (
                        make_response(jsonify(responseObject)),
                        HTTPStatus.UNAUTHORIZED,
                    )

            except Exception as e:
                responseObject = {"status": "failed", "message": format(e)}
                return make_response(jsonify(responseObject)), HTTPStatus.UNAUTHORIZED

            # returns the current logged in users contex to the routes
            return view_func(current_user, *args, **kwargs)

        return decorated

    return decorator


# validate user permission with roles
def validate_user_permission(feature_name, role_name):
    feature = Feature.query.filter_by(name=feature_name).first()
    role = Role.query.filter_by(name=role_name).first()

    if feature and role:
        access = FeatureRole.query.filter_by(feature=feature, role=role).first()
        return False if access is None else True

    return False


def get_user_info(token):
    payload = decode_jwt_token(token)
    user = User.query.filter_by(email=payload["userEmail"], active=True).first()
    return user.serialize if user is not None else None


def get_jwt_token(request):
    token = None
    if "Authorization" in request.headers and request.headers[
        "Authorization"
    ].startswith("Bearer "):
        token = request.headers["Authorization"].split(None, 1)[1].strip()
    elif "token" in request.form:
        token = request.form["token"]
    elif "token" in request.args:
        token = request.args["token"]

    return token


def encode_jwt_token(user):
    try:
        payload = {
            "exp": datetime.datetime.now(timezone.utc)
            + datetime.timedelta(days=30, hours=0, minutes=0, seconds=0),
            "iat": datetime.datetime.now(timezone.utc),
            "userEmail": user.email,
            "userId": user.id,
            "userName": user.name,
            "userRole": user.role.name,
        }
        return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    except Exception as e:
        raise (e)


def decode_jwt_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError as e:
        raise (e)
    except jwt.InvalidTokenError as e:
        raise (e)
