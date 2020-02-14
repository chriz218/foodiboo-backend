from models.base_model import BaseModel
import peewee as pw

class Food(BaseModel):
    name = pw.CharField(unique=False)
    geolocation = pw.CharField(unique=False, null=True)
    longitude = pw.DecimalField(null=True)
    latitude = pw.DecimalField(null=True)
    price = pw.DecimalField(decimal_places=2, null=True)
