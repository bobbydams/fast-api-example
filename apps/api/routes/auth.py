from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_refresh_token_required,
)

from apps.api.app import bp


@bp.route('/login', methods=['POST'])
@swag_from('specs/login_post.yml', methods=['POST'])
def login():
    if not request.is_json:
        return {"message": "Missing JSON in request"}, 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return {"message": "Missing username parameter"}, 400
    if not password:
        return {"message": "Missing password parameter"}, 400

    if username != 'test' or password != 'test':
        return {"message": "Bad username or password"}, 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return dict(access_token=access_token, refresh_token=refresh_token), 200


@bp.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    ret = {'access_token': create_access_token(identity=current_user)}
    return ret, 200
