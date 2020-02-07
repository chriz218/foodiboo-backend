from models.base_model import BaseModel
import peewee as pw
import re
from werkzeug.security import generate_password_hash

class User(BaseModel):
    name = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField(unique=False)
    profile_image = pw.CharField(null=True)

    def validate(self):
        duplicate_username = User.get_or_none(User.name == self.name)
        duplicate_email = User.get_or_none(User.email == self.email)
        email_format = '[A-Za-z0-9]+[A-Za-z0-9\_\.\-]+@+[a-z]+[.]+.[A-Za-z\.]+'
        # password_format = '[A-Za-z0-9@#$%^&+=]{8,}'   ## TO BE ADDED EVENTUALLY

        if duplicate_username:
            self.errors.append('Username already exist')

        if duplicate_email:
            self.errors.append('Email address already in use')

        if self.email and re.search(email_format, self.email) is None:
            self.errors.append('Invalid email address')

        if self.password and len(self.password) < 8:
            self.errors.append('Password needs to have at least 8 characters')

        if self.confirm_password != self.password:
            self.errors.append('Passwords do not match')       
        
        if self.password:
            self.password = generate_password_hash(self.password)