from mongoengine import *
from uuid import uuid4
from datetime import datetime


class Role:
    id = StringField(primary_key=True, default=lambda:str(uuid4()))  
    name = StringField(unique=True, required=True)
    addedTime = DateTimeField(default=datetime.now())
    updatedTime = DateTimeField()