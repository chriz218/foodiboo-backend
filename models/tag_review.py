from models.base_model import BaseModel
from models.tag import Tag
from models.review import Review
import peewee as pw


class TagReview(BaseModel):
    review = pw.ForeignKeyField(Review, backref="all_reviews")
    tag = pw.ForeignKeyField(Tag, backref="all_tags")