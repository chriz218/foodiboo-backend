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
from foodiboo_api.util.helpers import *
from config import S3_BUCKET_NAME, S3_LOCATION

food_dishes_api_blueprint = Blueprint('food_dishes',
                            __name__,
                            template_folder='templates')

# # Renders the create review page 
# @food_dishes_api_blueprint.route('/new', methods=['GET'])
# def new():
#     return render_template('food_dishes/new.html')

# Create a review
@food_dishes_api_blueprint.route('/create', methods=['POST'])
# def create():
#     logged_in_user_id = request.json.get("user_id")
#     food_name = request.json.get('food_name')
#     criterion_z1 = request.json.get('criterion_z1')
#     criterion_z2 = request.json.get('criterion_z2')
#     criterion_z3 = request.json.get('criterion_z3')
#     criterion_z4 = request.json.get('criterion_z4')
#     criterion_z5 = request.json.get('criterion_z5')
#     food_picture = request.json.get('food_picture')
#     latitude = request.json.get('latitude')
#     longitude = request.json.get('longitude')
#     price = request.json.get('price')
#     tag_list = request.json.get('tag_list')



#     ## This line below will not work                        ## Need to put a range here
#     food_already_exist = Food.get_or_none(name = food_name, latitude = latitude, longitude = longitude, price = price)
    
    
    
#     if food_already_exist:

#         review_already_exist = Review.get_or_none(user_id = logged_in_user_id, food_id = food_already_exist.id)

#         if review_already_exist:
#             return jsonify({"err": "You have already submitted a review for this dish in this location"}), 400
#         else: 
#             new_review_instance = Review(user_id = logged_in_user_id, food_picture = food_picture, criterion_z1 = criterion_z1, criterion_z2 = criterion_z2, criterion_z3 = criterion_z3, criterion_z4 = criterion_z4, criterion_z5 = criterion_z5, food_id = food_already_exist.id)
#             if new_review_instance.save():
#                 # if "user_file" not in request.files:
#                 #     return jsonify({"err": "No user_file key in request.files"}),400
#                 file = request.files['user_file']
#                 if file.filename == "":
#                     return jsonify({"err": "Please select a file"}),400
#                 if file and allowed_file(file.filename):
#                     file.filename = secure_filename(file.filename)
#                     output = upload_file_to_s3(file,S3_BUCKET_NAME)
#                     food_picture = str(output)
#                     new_review_instance = Review(user_id = logged_in_user_id, food_picture = food_picture, criterion_z1 = criterion_z1, criterion_z2 = criterion_z2, criterion_z3 = criterion_z3, criterion_z4 = criterion_z4, criterion_z5 = criterion_z5, food_id = food_already_exist.id)
#                     if new_review_instance.save():
#                     # Creation of tag    
#                         for tag_element in tag_list:
#                             tag_already_exist = Tag.get_or_none(name = tag_element)
#                             if tag_already_exist:
#                                 new_tag_review_instance = TagReview(review_id = new_review_instance.id, tag_id = tag_already_exist.id)
#                                 new_tag_review_instance.save()
#                             else:
#                                 new_tag_instance = Tag(name = tag_element)
#                                 new_tag_instance.save()
#                                 new_tag_instance_id = Tag.get_or_none(name = tag_element).id
#                                 new_tag_review_instance = TagReview(review_id = new_review_instance.id, tag_id = new_tag_instance_id)
#                                 new_tag_review_instance.save()
#                     # if food image upload success       
#                         return jsonify({
#                             "logged_in_user_id": logged_in_user_id,
#                             "food_picture": food_picture,
#                             "criterion_z1": criterion_z1,
#                             "criterion_z2": criterion_z2,
#                             "criterion_z3": criterion_z3,
#                             "criterion_z4": criterion_z4,
#                             "criterion_z5": criterion_z5,
#                             "food_id": food_already_exist.id,
#                             "price": price,
#                             "latitude": latitude,
#                             "longitude": longitude,
#                             "tag_list": tag_list
#                         }), 200
#                     else:
#                         # if jsonify error 
#                         return jsonify({"err": "Something went wrong"}), 400
#                 else:
#                     return jsonify({"err": "Something went wrong"}), 400
#                     # if image fail to upload
#     else:
#         new_food_instance = Food(name = food_name, longitude = longitude, latitude = latitude, price = price)
#         if new_food_instance.save(): 
#             if "user_file" not in request.files:
#                 return jsonify({"err": "No user_file key in request.files"}),400
#             file = request.files['user_file']
#             if file.filename == "":
#                 return jsonify({"err": "Please select a file"}),400
#             if file and allowed_file(file.filename):
#                 file.filename = secure_filename(file.filename)
#                 output = upload_file_to_s3(file,S3_BUCKET_NAME)
#                 food_picture = str(output)
#                 new_food_instance_id = Food.get_or_none(name = food_name, longitude = longitude, latitude = latitude).id
#                 new_review_instance = Review(user_id = logged_in_user_id, food_picture = food_picture, criterion_z1 = criterion_z1, criterion_z2 = criterion_z2, criterion_z3 = criterion_z3, criterion_z4 = criterion_z4, criterion_z5 = criterion_z5, food_id = new_food_instance_id)
#                 if new_review_instance.save():
#                 # Creation of tag    
#                     for tag_element in tag_list:
#                         tag_already_exist = Tag.get_or_none(name = tag_element)
#                         if tag_already_exist:
#                             new_tag_review_instance = TagReview(review_id = new_review_instance.id, tag_id = tag_already_exist.id)
#                             new_tag_review_instance.save()
#                         else:
#                             new_tag_instance = Tag(name = tag_element)
#                             new_tag_instance.save()
#                             new_tag_instance_id = Tag.get_or_none(name = tag_element).id
#                             new_tag_review_instance = TagReview(review_id = new_review_instance.id, tag_id = new_tag_instance_id)
#                             new_tag_review_instance.save()   
#                 # if food image upload success       
#                     return jsonify({
#                         "logged_in_user_id": logged_in_user_id,
#                         "food_picture": food_picture,
#                         "criterion_z1": criterion_z1,
#                         "criterion_z2": criterion_z2,
#                         "criterion_z3": criterion_z3,
#                         "criterion_z4": criterion_z4,
#                         "criterion_z5": criterion_z5,
#                         "food_id": new_food_instance_id,
#                         "price": price,
#                         "latitude": latitude,
#                         "longitude": longitude,
#                         "tag_list": tag_list
#                     }), 200
#                 else:
#                     # if jsonify error 
#                     return jsonify({"err": "Something went wrong"}), 400
#             else:
#                 return jsonify({"err": "Something went wrong"}),400
#                 # if image fail to upload
#         else:
#             return jsonify({"err": "Something went wrong"}), 400
#             # if review instance failed to save


def create():

    logged_in_user_id = request.form.get('user_id')
    food_name = request.form.get('food_name')
    criterion_z1 =  int(request.form.get('criterion_z1'))
    criterion_z2 =  int(request.form.get('criterion_z2'))
    criterion_z3 =  int(request.form.get('criterion_z3'))
    criterion_z4 =  int(request.form.get('criterion_z4'))
    criterion_z5 =  int(request.form.get('criterion_z5'))
    food_picture =  request.files['food_picture']
    latitude =  float(request.form.get('latitude'))
    longitude = float(request.form.get('longitude'))
    price = float(request.form.get('price'))

    # logged_in_user_id = request.json.get("user_id")
    # food_name = request.json.get('food_name')
    # criterion_z1 = request.json.get('criterion_z1')
    # criterion_z2 = request.json.get('criterion_z2')
    # criterion_z3 = request.json.get('criterion_z3')
    # criterion_z4 = request.json.get('criterion_z4')
    # criterion_z5 = request.json.get('criterion_z5')
    # food_picture = request.json.get('food_picture')
    # latitude = request.json.get('latitude')
    # longitude = request.json.get('longitude')
    # price = request.json.get('price')
    # tag_list = request.json.get('tag_list')
                      
    food_already_exist = Food.select().where(Food.name == food_name, Food.latitude > latitude - 0.0002, Food.latitude < latitude + 0.0002, Food.longitude > longitude - 0.0002, Food.longitude < longitude + 0.0002)

    food_already_exist_id_arr = [food_already_exist_element.id for food_already_exist_element in food_already_exist]

    jsonify({"err":"test1"})
    if food_already_exist:

        review_already_exist = Review.get_or_none(user_id = logged_in_user_id, food_id = food_already_exist.id)
        jsonify({"err":"test2"})

        if review_already_exist:
            return jsonify({"err": "You have already submitted a review for this dish in this location"}), 400
        else: 
            new_review_instance = Review(user_id = logged_in_user_id, food_picture = food_picture, criterion_z1 = criterion_z1, criterion_z2 = criterion_z2, criterion_z3 = criterion_z3, criterion_z4 = criterion_z4, criterion_z5 = criterion_z5, food_id = food_already_exist_id_arr[0])
            if new_review_instance.save():
                file = request.files['food_picture']
                if file and allowed_file(file.filename):
                    file.filename = secure_filename(file.filename)
                    output = upload_file_to_s3(file,S3_BUCKET_NAME)
                    food_picture = str(output)
                    new_review_instance = Review(user_id = logged_in_user_id, food_picture = food_picture, criterion_z1 = criterion_z1, criterion_z2 = criterion_z2, criterion_z3 = criterion_z3, criterion_z4 = criterion_z4, criterion_z5 = criterion_z5, food_id = food_already_exist_id_arr[0])
                    if new_review_instance.save():
                    # Creation of tag    
                        # for tag_element in tag_list:
                        #     tag_already_exist = Tag.get_or_none(name = tag_element)
                        #     if tag_already_exist:
                        #         new_tag_review_instance = TagReview(review_id = new_review_instance.id, tag_id = tag_already_exist.id)
                        #         new_tag_review_instance.save()
                        #     else:
                        #         new_tag_instance = Tag(name = tag_element)
                        #         new_tag_instance.save()
                        #         new_tag_instance_id = Tag.get_or_none(name = tag_element).id
                        #         new_tag_review_instance = TagReview(review_id = new_review_instance.id, tag_id = new_tag_instance_id)
                        #         new_tag_review_instance.save()
                    # if food image upload success       
                        return jsonify({
                            "logged_in_user_id": logged_in_user_id,
                            "food_picture": food_picture,
                            "criterion_z1": criterion_z1,
                            "criterion_z2": criterion_z2,
                            "criterion_z3": criterion_z3,
                            "criterion_z4": criterion_z4,
                            "criterion_z5": criterion_z5,
                            "food_id": food_already_exist.id,
                            "price": price,
                            "latitude": latitude,
                            "longitude": longitude
                            # "tag_list": tag_list
                        }), 200
                    else:
                        # if jsonify error 
                        return jsonify({"err": "Something went wrong"}), 400
                else:
                    return jsonify({"err": "Something went wrong"}), 400
                    # if image fail to upload
    else:
        new_food_instance = Food(name = food_name, longitude = longitude, latitude = latitude, price = price)
        if new_food_instance.save(): 
            print(food_picture)
            # print(food_picture.files)
            file = request.files['food_picture']            
            print(file.filename)
            if file and allowed_file(file.filename):
                file.filename = secure_filename(file.filename)
                output = upload_file_to_s3(file,S3_BUCKET_NAME)
                food_picture = str(output)
                
                print(latitude, "LATTITUDE")
                print(longitude, "LONGITUDE")
                print(type(latitude), "LATITUDE TYPE OF")
                print(type(longitude), "LONTITUDE TYPE OF")
                
                new_food_instance_id = Food.get(name = food_name, longitude = longitude, latitude = latitude)
                print(new_review_instance, "REVIEW INSTANCE")
                print(new_review_instance.id, "REVIEW INSTANCE ID")
                new_review_instance = Review(user_id = logged_in_user_id, food_picture = food_picture, criterion_z1 = criterion_z1, criterion_z2 = criterion_z2, criterion_z3 = criterion_z3, criterion_z4 = criterion_z4, criterion_z5 = criterion_z5, food_id = new_food_instance_id.id)
                if new_review_instance.save():
                # Creation of tag    
                    # for tag_element in tag_list:
                    #     tag_already_exist = Tag.get_or_none(name = tag_element)
                    #     if tag_already_exist:
                    #         new_tag_review_instance = TagReview(review_id = new_review_instance.id, tag_id = tag_already_exist.id)
                    #         new_tag_review_instance.save()
                    #     else:
                    #         new_tag_instance = Tag(name = tag_element)
                    #         new_tag_instance.save()
                    #         new_tag_instance_id = Tag.get_or_none(name = tag_element).id
                    #         new_tag_review_instance = TagReview(review_id = new_review_instance.id, tag_id = new_tag_instance_id)
                    #         new_tag_review_instance.save()   
                # if food image upload success       
                    return jsonify({
                        "logged_in_user_id": logged_in_user_id,
                        "food_picture": food_picture,
                        "criterion_z1": criterion_z1,
                        "criterion_z2": criterion_z2,
                        "criterion_z3": criterion_z3,
                        "criterion_z4": criterion_z4,
                        "criterion_z5": criterion_z5,
                        "food_id": new_food_instance_id,
                        "price": price,
                        "latitude": latitude,
                        "longitude": longitude
                        # "tag_list": tag_list
                    }), 200
                else:
                    # if jsonify error 
                    return jsonify({"err": "Something went wrong"}), 400
            else:
                return jsonify({"err": "Something went wrong"}),400
                # if image fail to upload
        else:
            return jsonify({"err": "Something went wrong"}), 400
            # if review instance failed to save



# @images_api_blueprint.route('/picture', methods=['POST'])
# @jwt_required
# def create():
#     # upload image
#     user_id = get_jwt_identity()
#     if user_id:
#         user = User.get_or_none(id=user_id)
#         if user:
#             file = request.files['image']
#             if file and allowed_file(file.filename):
#                 output = upload_file_to_s3(file,os.getenv("AWS_BUCKET_NAME"))
#                 if output==True:
#                     Image(image_path=file.filename,user = user.id).save()
#                     responseObject = {
#                         'success': 'ok',
#                         'message': 'Your photo successfully uploaded.'
#                     }
#                     return jsonify(responseObject)
#                 else:
#                     responseObject = {
#                         'status': 'failed',
#                         'message': 'Upload failed'
#                     }
#             else:
#                 responseObject = {
#                     'status': 'failed',
#                     'message': 'No file found'
#                 }
#         else:
#             responseObject = {
#                 'status': 'failed',
#                 'message': 'Authentication failed'
#             }
#             return jsonify(responseObject), 401
#     else:
#         responseObject = {
#             'status': 'failed',
#             'message': 'No authorization header found'
#         }
#         return jsonify(responseObject), 401



# Renders the food dish page
@food_dishes_api_blueprint.route('/<food_name>', methods=["GET"])
def show(food_name):
    # food_name = request.json.get('food_name')
    all_of_that_food = Food.select().where(Food.name == food_name)
    
    if len(all_of_that_food) != 0:
        food_id_arr = [food.id for food in all_of_that_food]
        food_price_arr = [food.price for food in all_of_that_food]
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
        first_review_food_pic = []

        for food_id_element in food_id_arr:
            criterion_z1_list.append([e.criterion_z1 for e in Review.select().join(Food, on=(Food.id == Review.food_id)).where(Food.id == food_id_element)])
            criterion_z2_list.append([e.criterion_z2 for e in Review.select().join(Food, on=(Food.id == Review.food_id)).where(Food.id == food_id_element)])
            criterion_z3_list.append([e.criterion_z3 for e in Review.select().join(Food, on=(Food.id == Review.food_id)).where(Food.id == food_id_element)])
            criterion_z4_list.append([e.criterion_z4 for e in Review.select().join(Food, on=(Food.id == Review.food_id)).where(Food.id == food_id_element)])
            criterion_z5_list.append([e.criterion_z5 for e in Review.select().join(Food, on=(Food.id == Review.food_id)).where(Food.id == food_id_element)])
            first_review_food_pic.append(S3_LOCATION + [e.food_picture for e in Review.select().join(Food, on=(Food.id == Review.food_id)).where(Food.id == food_id_element)][0])

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
            "average_c5": average_c5,
            "first_review_food_pic": first_review_food_pic
        })
    else:
        return jsonify({
            "err": "Food dish does not exist"
        }), 400 

@food_dishes_api_blueprint.route('/<food_name>/<id>', methods=["GET"])
def show_spec(food_name, id):
    food = Food.get_or_none(id == id)

    if food:
        reviews = Review.select().where(Review.food_id == id)
        criterion_z1_list = [e.criterion_z1 for e in reviews]
        criterion_z2_list = [e.criterion_z2 for e in reviews]
        criterion_z3_list = [e.criterion_z3 for e in reviews]
        criterion_z4_list = [e.criterion_z4 for e in reviews]
        criterion_z5_list = [e.criterion_z5 for e in reviews]
        reviewers_list = []
        food_pic_list = []

        for i in [e.food_picture for e in reviews]:
            food_pic_list.append(S3_LOCATION + i)

        for i in [reviewer.user_id for reviewer in reviews]:
            reviewers_list.append(User.get_by_id(i).name)

        return jsonify({
            "criterion_z1_list": criterion_z1_list,
            "criterion_z2_list": criterion_z2_list,
            "criterion_z3_list": criterion_z3_list,
            "criterion_z4_list": criterion_z4_list,
            "criterion_z5_list": criterion_z5_list,
            "reviewers_list": reviewers_list,
            "food_pic_list": food_pic_list
        })

    else:
        return jsonify({
            "err": "Food dish does not exist"
        }), 400    