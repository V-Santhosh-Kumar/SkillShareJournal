from mongoengine import *
from uuid import uuid4
from datetime import datetime


class Role(Document):
    id = StringField(primary_key=True, default=lambda:str(uuid4()))  
    name = StringField(unique=True, required=True)
    addedTime = DateTimeField(default=datetime.now())
    updatedTime = DateTimeField()

class User(Document):
    id = StringField(primary_key=True, default=lambda:str(uuid4()))    
    username = StringField(unique=True, required=True)
    email = EmailField(unique=True, required=True)
    password = StringField(required=True)
    phone = StringField()
    role = ReferenceField(Role, null=True)
    addedTime = DateTimeField(default=datetime.now())
    updatedTime = DateTimeField()

    
    