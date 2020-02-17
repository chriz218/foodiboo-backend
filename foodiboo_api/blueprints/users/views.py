from flask import Blueprint, Flask, request, json, jsonify
from werkzeug.security import generate_password_hash # This function allows one to hash a password
from models.user import User
from models.food import Food
from models.review import Review
from models.tag import Tag
from flask_login import current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from config import S3_BUCKET_NAME, S3_LOCATION
# from foodiboo_web.util.helpers import *

users_api_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_api_blueprint.route('/sign_up', methods=['POST'])
def sign_up():
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
        }), 400


@users_api_blueprint.route('/<username>', methods=["GET"])
def show(username):
    user = User.get_or_none(name = username)
    if user is not None:
        reviews = user.all_user_reviews 
        review_food_pic_list = []
        food_name_list = []
        food_latitude_list = []
        food_longitude_list = []
        food_price_list = []

        for review in [review.food_picture for review in reviews]:
            review_food_pic_list.append(S3_LOCATION + review)

        for review_id in [review.food_id for review in reviews]:
            food = Food.get_or_none(Food.id == review_id)
            food_name_list.append(food.name)
            food_latitude_list.append(food.latitude)
            food_longitude_list.append(food.longitude)
            food_price_list.append(str(food.price))

        return jsonify({
            "name": user.name,
            # "profile_image": user.profile_image,
            "review_id_list": [review.id for review in reviews],
            "food_id_list": [review.food_id for review in reviews],
            "review_criterion_z1_list": [review.criterion_z1 for review in reviews],
            "review_criterion_z2_list": [review.criterion_z2 for review in reviews],
            "review_criterion_z3_list": [review.criterion_z3 for review in reviews],
            "review_criterion_z4_list": [review.criterion_z4 for review in reviews],
            "review_criterion_z5_list": [review.criterion_z5 for review in reviews],
            "review_food_pic_list": review_food_pic_list,
            "food_name_list": food_name_list,
            "food_latitude_list": food_latitude_list,
            "food_longitude_list": food_longitude_list,
            "food_price_list": food_price_list
            # "reviews": reviews
        })
    else:
        return jsonify({"err": "Something went wrong"}), 400





