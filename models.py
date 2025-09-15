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

class Note(Document):
    id = StringField(primary_key=True, default=lambda:str(uuid4()))
    title = StringField(unique=True, required=True)
    description = StringField(required=True)
    code = StringField()
    image = ListField(StringField())
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    addedTime = DateTimeField(default=datetime.now())
    updatedTime = DateTimeField()

class Like(Document):
    id = StringField(primary_key=True, default=lambda:str(uuid4()))   
    user = ReferenceField(User)
    count = IntField(default=0)
    note = ReferenceField(Note, reverse_delete_rule=CASCADE)
    addedTime = DateTimeField(default=datetime.now())
    updatedTime = DateTimeField()

class Comment(Document):
    id = StringField(primary_key=True, default=lambda:str(uuid4()))   
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    comment = StringField()
    note = ReferenceField(Note, reverse_delete_rule=CASCADE)
    addedTime = DateTimeField(default=datetime.now())
    updatedTime = DateTimeField()

class Tags(Document):
    id = StringField(primary_key=True, default=lambda:str(uuid4()))    
    name = StringField(unique=True, required=True)
    description = StringField()
    addedTime = DateTimeField(default=datetime.now())
    updatedTime = DateTimeField()

class SavedNotes(Document):
    id = StringField(primary_key=True, default=lambda:str(uuid4()))  
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
    Notes = ReferenceField(Note, reverse_delete_rule=CASCADE)
    addedTime = DateTimeField(default=datetime.now())
    updatedTime = DateTimeField()
