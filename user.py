from models import *
from flask import Flask, request, jsonify
from mongoengine import *
from uuid import uuid4
from datetime import datetime



app = Flask(__name__)

@app.post("/user/new")
def addUser():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')
        role_id = data.get('role_id')

        if not username or not email or not password:
            return jsonify({"status": "error", "message": "All Fields are Required"})

        if role_id:
            role = Role.objects(id=role_id).first()
            if not role:
                return jsonify({"status": "error", "message": "Invalid Role"})

        user = User(username=username, email=email, password=password, phone=phone, role=role)
        user.save()


        return jsonify({"status": "success", "message": "User Added Successfully"})
    
    except Exception as e:

        return jsonify({"status": "error", "message": str(e)})

@app.get("/user/getAll")
def get_all_users():
    try:
        users = User.objects()
        user_list = []
        
        for user in users:
            data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "role": user.role.name,
                "addedTime": user.addedTime,
                "updatedTime": user.updatedTime
            }
            user_list.append(data)

        return jsonify({"status": "success", "message": "Users Retrieved Successfully", "data": user_list})
    
    except Exception as e:
        
        return jsonify({"status": "error", "message": str(e)})

    