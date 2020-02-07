from models.base_model import BaseModel
import peewee as pw


class Tag(BaseModel):
    name = pw.CharField()


