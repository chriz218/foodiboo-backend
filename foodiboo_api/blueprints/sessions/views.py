from app import app 
from flask import Blueprint, Flask, request, json, jsonify
from werkzeug.security import generate_password_hash # This function allows one to hash a password
from models.user import User
from models.food import Food
from models.review import Review
from models.tag import Tag
from flask_login import current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt, jwt_refresh_token_required
)
from config import JWT_SECRET_KEY 

sessions_api_blueprint = Blueprint('sessions',
                            __name__,
                            template_folder='templates')

jwt = JWTManager(app)

@sessions_api_blueprint.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    name = request.json.get('name')
    password = request.json.get('password')

    user = User.get_or_none(User.name == name)

    if user is None:
        return jsonify({
                "err": "Username does not exist"
        }), 400
    else:
        # hashed_password = user.password    
        result = check_password_hash(user.password, password)
        if result == True:
            access_token = create_access_token(identity=name)
            return jsonify({
                "status": "Success",
                "token": access_token,
                "user": {"name": user.name, "email": user.email, "id":user.id}
            }), 200
        else:
            return jsonify({
                "err": "Wrong username or password"
            }), 400


@sessions_api_blueprint.route('/protected', methods=['GET'])
@jwt_required
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# # Endpoint for revoking the current users access token
# @sessions_api_blueprint.route('/logout', methods=['DELETE'])
# @jwt_required
# def logout():
#     jti = get_raw_jwt()['jti']
#     blacklist.add(jti)
#     return jsonify({"msg": "Successfully logged out"}), 200


# # Endpoint for revoking the current users refresh token
# @sessions_api_blueprint.route('/logout2', methods=['DELETE'])
# @jwt_refresh_token_required
# def logout2():
#     jti = get_raw_jwt()['jti']
#     blacklist.add(jti)
#     return jsonify({"msg": "Successfully logged out"}), 200    


