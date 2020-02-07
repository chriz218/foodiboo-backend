# Views for the Food Dishes
from flask import Blueprint, render_template, Flask, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash # This function allows one to hash a password
from models.user import User
from models.food import Food
from models.review import Review
from models.tag_review import TagReview
from models.tag import Tag
from flask_login import current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
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
#     if food_already_exist():
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
    all_of_that_food = Food.select().where(name = food_name)
    
    
    # all_foods = food.all_foods
    # all_reviews = review.all_reviews
    # food_review = FoodReview.get_or_none(food_id = food.id)
    # if food is not None:
    #     review = Review.get_or_none(id = food_review.review_id)
    #     return render_template('food_dishes/foodprofile.html', food = food, review = review) ## Need to create a page to display all reviews for a dish
    # else:
    #     flash("Food dish does not exist")
    #     return redirect(url_for('home'))    

# Search box
@food_dishes_blueprint.route('/search', methods=["GET"])
def search():
    food_search = request.args.get('food_search')
    return redirect(url_for('food_dishes.show', food_name = food_search))


@food_dishes_blueprint.route('/', methods=["GET"])
def index():
    return "FOOD_DISHES"


@food_dishes_blueprint.route('/<id>/edit', methods=['GET'])
def edit(id):
    pass


@food_dishes_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
