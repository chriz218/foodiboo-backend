from models.base_model import BaseModel
import peewee as pw


class Food(BaseModel):
    name = pw.CharField(unique=False)
    geolocation = pw.CharField(unique=False, null=True)
