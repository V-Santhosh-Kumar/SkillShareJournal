from models import *
from mongoengine import *
from flask import request, jsonify, Blueprint
from datetime import datetime


user_bp = Blueprint('user_bp', __name__)

@user_bp.post("/user/new")
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

@user_bp.get("/user/getAll")
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
                "roleId": user.role.id,
                "addedTime": user.addedTime,
                "updatedTime": user.updatedTime
            }
            user_list.append(data)
        total = User.objects().count()
        return jsonify({
            "status": "success", 
            "message": "Users Retrieved Successfully", 
            "data": user_list,
            "recordsTotal": total,
            "recordsFiltered": total,
            "draw": int(request.args.get("draw", 1))
        })
    
    except Exception as e:
        
        return jsonify({"status": "error", "message": str(e)})


@user_bp.get('/user/getSpecific')
def getSpecificUser():
    try:
        id = request.args.get('id')

        if not id:
            return jsonify({"status": "error", "message": "Id is Required"})

        user = User.objects(id=id).first()

        if not user:
            return jsonify({"status": "error", "message": "User not found."})

        like = Like.objects().count()
        savedNotes = SavedNotes.objects().count()
        comment = Comment.objects().count()


        data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone": user.phone,
                "role": user.role.name,
                "addedTime": user.addedTime,
                "updatedTime": user.updatedTime,
                "likeCount": like,
                "savedNotesCount": savedNotes,
                "commentCount": comment
            }
        
        return jsonify({"status": "success", "message": "User Retrieved Successfully", "data": data})
    
    except Exception as e:

        return jsonify({"status": "error", "message": str(e)})


@user_bp.put('/user/update')
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
        role.updatedTime = datetime.now()
        user.save()

        return jsonify({"status": "success", "message": "User Updated Successfully"})
    
    except Exception as e:

        return jsonify({"status": "error", "message": str(e)})
    
@user_bp.put('/user/delete')
def deleteUser():
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
    

