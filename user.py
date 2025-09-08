from models import *
from mongoengine import *
from flask import request, jsonify
from app import app

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

        if not role_id:
            return jsonify({"status": "error", "message": "Invalid Role"})

        role = Role.objects(id=role_id).first()

        if not role:
            return jsonify({"status": "error", "message": "Role not found."})

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


@app.get('/user/getSpecific')
def getSpecificUser():
    try:
        id = request.args.get('id')

        if not id:
            return jsonify({"status": "error", "message": "Id is Required"})

        user = User.objects(id=id).first()

        if not user:
            return jsonify({"status": "error", "message": "User not found."})

        data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "role": user.role.name,
                "addedTime": user.addedTime,
                "updatedTime": user.updatedTime
            }
        
        return jsonify({"status": "success", "message": "User Retrieved Successfully", "data": data})
    
    except Exception as e:

        return jsonify({"status": "error", "message": str(e)})


@app.put('/user/update')
def updateUser():
    try:
        id = request.args.get('id')

        if not id:
            return jsonify({"status": "error", "message": "Id is Required"})
        
        user = User.objects(id=id).first()

        if not User:
            return jsonify({"status": "error", "message": "User not found."})
        
        data = request.get_json()
        role_id = data.get("role_id")
        if not role_id:
            return jsonify({"status": "error", "message": "Invalid Role"})

        role = Role.objects(id=role_id).first()

        if not role:
            return jsonify({"status": "error", "message": "Role not found."})
        
        user.role = role
        user.phone = data["phone"]
        user.save()

        return jsonify({"status": "success", "message": "User Updated Successfully"})
    
    except Exception as e:

        return jsonify({"status": "error", "message": str(e)})
    
@app.put('/user/delete')
def updateUser():
    try:
        id = request.args.get('id')

        if not id:
            return jsonify({"status": "error", "message": "Id is Required"})

        user = User.objects(id=id).first()

        if not user:
            return jsonify({"status": "error", "message": "User not found."})
        
        user.delete()

        return jsonify({"status": "success", "message": "User Deleted Successfully"})
    
    except Exception as e:

        return jsonify({"status": "error", "message": str(e)})