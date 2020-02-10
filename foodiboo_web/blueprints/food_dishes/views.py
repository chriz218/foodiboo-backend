# Views for the Food Dishes
from flask import Blueprint, Flask, request, json, jsonify
from werkzeug.security import generate_password_hash # This function allows one to hash a password
from models.user import User
from models.food import Food
from models.review import Review
from models.tag_review import TagReview
from models.tag import Tag
from flask_login import current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from math import floor
# from foodiboo_web.util.helpers import *

food_dishes_blueprint = Blueprint('food_dishes',
                            __name__,
                            template_folder='templates')


# Renders the create review page 
@food_dishes_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('food_dishes/new.html')

# Create a review
@food_dishes_blueprint.route('/create', methods=['POST'])
# def create():
#     food_name = request.json.get('food_name')
#     criterion_z1 = request.json.get('criterion_z1')
#     criterion_z2 = request.json.get('criterion_z2')
#     criterion_z3 = request.json.get('criterion_z3')
#     criterion_z4 = request.json.get('criterion_z4')
#     criterion_z5 = request.json.get('criterion_z5')
#     food_picture = request.json.get('food_picture')
#     geolocation = request.json.get('location')
#     food_already_exist = Food.get_or_none(name = food_name, geolocation = geolocation)
#     if food_already_exist:
#         new_review_instance = Review(user_id = current_user.id, food_picture = food_picture, criterion_z1 = criterion_z1, criterion_z2 = criterion_z2, criterion_z3 = criterion_z3, criterion_z4 = criterion_z4, criterion_z5 = criterion_z5, food_id = food_already_exist.id)
#         if new_review_instance.save():
#             return jsonify({
#                 "user_id": current_user.id,
#                 "food_picture": food_picture,
#                 "criterion_z1": criterion_z1,
#                 "criterion_z2": criterion_z2,
#                 "criterion_z3": criterion_z3,
#                 "criterion_z4": criterion_z4,
#                 "criterion_z5": criterion_z5,
#                 "food_id": food_already_exist.id
#             }), 200
#         else:
#             return jsonify({"err": "Something went wrong"}), 500
#     else:
#         new_food_instance = Food(name = food_name, geolocation = geolocation)
#         if new_food_instance.save():
#             new_review_instance = Review(user_id = current_user.id, food_picture = food_picture, criterion_z1 = criterion_z1, criterion_z2 = criterion_z2, criterion_z3 = criterion_z3, criterion_z4 = criterion_z4, criterion_z5 = criterion_z5, food_id = new_food_instance.id)
#             if new_review_instance.save():
#                 return jsonify({
#                     "user_id": current_user.id,
#                     "food_picture": food_picture,
#                     "criterion_z1": criterion_z1,
#                     "criterion_z2": criterion_z2,
#                     "criterion_z3": criterion_z3,
#                     "criterion_z4": criterion_z4,
#                     "criterion_z5": criterion_z5,
#                     "food_id": food_already_exist.id
#                 }), 200
#             else:
#                 return jsonify({"err": "Something went wrong"}), 500
#         else:
#             return jsonify({"err": "Something went wrong"}), 500

def create():
    food_name = request.json.get('food_name')
    criterion_z1 = request.json.get('criterion_z1')
    criterion_z2 = request.json.get('criterion_z2')
    criterion_z3 = request.json.get('criterion_z3')
    criterion_z4 = request.json.get('criterion_z4')
    criterion_z5 = request.json.get('criterion_z5')
    food_picture = request.json.get('food_picture')
    geolocation = request.json.get('location')
    food_already_exist = Food.get_or_none(name = food_name, geolocation = geolocation)
    if food_already_exist:

        review_already_exist = Review.get_or_none(user_id = current_user.id, food_id = food_already_exist.id)

        if review_already_exist:
            return jsonify({"err": "You have already submitted a review for this dish in this location"}), 500
        else: 
            new_review_instance = Review(user_id = current_user.id, food_picture = food_picture, criterion_z1 = criterion_z1, criterion_z2 = criterion_z2, criterion_z3 = criterion_z3, criterion_z4 = criterion_z4, criterion_z5 = criterion_z5, food_id = food_already_exist.id)
            if new_review_instance.save():
                return jsonify({
                    "user_id": current_user.id,
                    "food_picture": food_picture,
                    "criterion_z1": criterion_z1,
                    "criterion_z2": criterion_z2,
                    "criterion_z3": criterion_z3,
                    "criterion_z4": criterion_z4,
                    "criterion_z5": criterion_z5,
                    "food_id": food_already_exist.id
                }), 200
            else:
                return jsonify({"err": "Something went wrong"}), 500
    else:
        new_food_instance = Food(name = food_name, geolocation = geolocation)
        if new_food_instance.save():
            new_review_instance = Review(user_id = current_user.id, food_picture = food_picture, criterion_z1 = criterion_z1, criterion_z2 = criterion_z2, criterion_z3 = criterion_z3, criterion_z4 = criterion_z4, criterion_z5 = criterion_z5, food_id = new_food_instance.id)
            if new_review_instance.save():
                return jsonify({
                    "user_id": current_user.id,
                    "food_picture": food_picture,
                    "criterion_z1": criterion_z1,
                    "criterion_z2": criterion_z2,
                    "criterion_z3": criterion_z3,
                    "criterion_z4": criterion_z4,
                    "criterion_z5": criterion_z5,
                    "food_id": food_already_exist.id
                }), 200
            else:
                return jsonify({"err": "Something went wrong"}), 500
        else:
            return jsonify({"err": "Something went wrong"}), 500
            
    
# Renders the food dish page
@food_dishes_blueprint.route('/<food_name>', methods=["GET"])
def show(food_name):
    all_of_that_food = Food.select().where(Food.name == food_name)
    
    if len(all_of_that_food) != 0:
        food_geolocation_arr = [food.geolocation for food in all_of_that_food]
        food_id_arr = [food.id for food in all_of_that_food]
        criterion_z1_list = []
        criterion_z2_list = []
        criterion_z3_list = []
        criterion_z4_list = []
        criterion_z5_list = []
        average_c1 = []
        average_c2 = []
        average_c3 = []
        average_c4 = []
        average_c5 = []

        for food_id_element in food_id_arr:
            criterion_z1_list.append([e.criterion_z1 for e in Review.select().join(Food, on=(Food.id == Review.food_id)).where(Food.id == food_id_element)])
            criterion_z2_list.append([e.criterion_z2 for e in Review.select().join(Food, on=(Food.id == Review.food_id)).where(Food.id == food_id_element)])
            criterion_z3_list.append([e.criterion_z3 for e in Review.select().join(Food, on=(Food.id == Review.food_id)).where(Food.id == food_id_element)])
            criterion_z4_list.append([e.criterion_z4 for e in Review.select().join(Food, on=(Food.id == Review.food_id)).where(Food.id == food_id_element)])
            criterion_z5_list.append([e.criterion_z5 for e in Review.select().join(Food, on=(Food.id == Review.food_id)).where(Food.id == food_id_element)])

        for criterion in criterion_z1_list:
            average_c1.append(floor(sum(criterion)/len(criterion)))
        for criterion in criterion_z2_list:
            average_c2.append(floor(sum(criterion)/len(criterion)))
        for criterion in criterion_z3_list:
            average_c3.append(floor(sum(criterion)/len(criterion)))
        for criterion in criterion_z4_list:
            average_c4.append(floor(sum(criterion)/len(criterion)))
        for criterion in criterion_z5_list:
            average_c5.append(floor(sum(criterion)/len(criterion)))


        return jsonify({
            # "all_of_that_food": all_of_that_food
            "food_geolocation_arr": food_geolocation_arr,
            "food_id_arr": food_id_arr,
            "criterion_z1_list": criterion_z1_list,
            "criterion_z2_list": criterion_z2_list,
            "criterion_z3_list": criterion_z3_list,
            "criterion_z4_list": criterion_z4_list,
            "criterion_z5_list": criterion_z5_list,
            "average_c1": average_c1,
            "average_c2": average_c2,
            "average_c3": average_c3,
            "average_c4": average_c4,
            "average_c5": average_c5
        })
    else:
        return jsonify({
            "err": "Food dish does not exist"
        }), 500    


@food_dishes_blueprint.route('/<food_name>/<id>', methods=["GET"])
def show_spec(id):
    food = Food.get_or_none(id == id)

    if food:
        reviews = Review.select().where(Review.food_id == id)
        criterion_z1_list = [e.criterion_z1 for e in reviews]
        criterion_z2_list = [e.criterion_z2 for e in reviews]
        criterion_z3_list = [e.criterion_z3 for e in reviews]
        criterion_z4_list = [e.criterion_z4 for e in reviews]
        criterion_z5_list = [e.criterion_z5 for e in reviews]
        reviewers_list = []

        for i in [reviewer.user_id for reviewer in reviews]:
            reviewers_list.append(User.get_by_id(i).name)

        return jsonify({
            "criterion_z1_list": criterion_z1_list,
            "criterion_z2_list": criterion_z2_list,
            "criterion_z3_list": criterion_z3_list,
            "criterion_z4_list": criterion_z4_list,
            "criterion_z5_list": criterion_z5_list,
            "reviewers_list": reviewers_list
        })

        
    else:
        return jsonify({
            "err": "Food dish does not exist"
        }), 500    