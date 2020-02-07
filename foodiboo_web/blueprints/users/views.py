from flask import Blueprint, render_template, Flask, request, flash, json, jsonify
from werkzeug.security import generate_password_hash # This function allows one to hash a password
from models.user import User
from models.food import Food
from models.review import Review
from models.tag import Tag
from flask_login import current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
# from foodiboo_web.util.helpers import *

users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')



# @users_blueprint.route('/signup', methods=['GET'])
# def new():
#     return render_template('users/new.html')


@users_blueprint.route('/create', methods=['POST'])
def create():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    confirm_password = request.json.get('confirm_password')
    new_user_instance = User(name = name, email = email, password = password, confirm_password = confirm_password)
    if new_user_instance.save():
        return jsonify({
                    "name": name,
                    "email": email,
                    "password": password
        }), 200
    else:
        return jsonify({
            'err': new_user_instance.errors
        }), 500
        # return jsonify(new_user_instance.errors), 500


@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(name = username)
    if user is not None:
        reviews = user.all_reviews 
        return jsonify({
            "name": user.name,
            "profile_image": user.profile_image,
            "reviews": reviews
        })
    else:
        return jsonify({"err": "Something went wrong"}), 500


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
