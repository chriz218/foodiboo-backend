from models.base_model import BaseModel
from models.user import User
from models.food import Food
import peewee as pw
import re
from playhouse.hybrid import hybrid_property # To get the url of uploaded pictures

class Review(BaseModel):
    user = pw.ForeignKeyField(User, backref="all_user_reviews")
    food = pw.ForeignKeyField(Food, backref="all_food_reviews", null=True)
    food_picture = pw.CharField()
    criterion_z1 = pw.IntegerField()
    criterion_z2 = pw.IntegerField()
    criterion_z3 = pw.IntegerField()
    criterion_z4 = pw.IntegerField()
    criterion_z5 = pw.IntegerField()

    # user.all_user_reviews will give all the reviews written by the user
    # food.all_food_reviews will give all the reviews of that food

