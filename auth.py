from models import User
from flask import request, jsonify, session, render_template, Blueprint


auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.post("/auth/login")
def login():
    try:

        data = request.get_json()
        email = data.get("email")
        password = data.get("password")


        if not email and not password:
            return jsonify({"status": "error", "message": "All Fields are Required"})

        
        user = User.objects(email=email).first()
        if not user:
            return jsonify({"status": "error", "message": "User not found. Please register to continue"})
        
        session["user"] = {
            "name": user.username,
            "email": user.email,
            "id": user.id
        }
        
        return jsonify({"status": "success", "message": "User Logged in Succcessfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
    
@auth_bp.post("/auth/register")
def register():
    try:

        data = request.get_json()
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        phone = data.get("phone")
        

        if not email and not password and not phone and not username :
            return jsonify({"status": "error", "message": "All Fields are Required"})

        user = User(
            username = username,
            email = email,
            password = password,
            phone = phone
        ).save()
        
        session["user"] = {
            "name": user.username,
            "email": user.email,
            "id": user.id
        }
        
        return jsonify({"status": "success", "message": "User Registered Succcessfully."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

@auth_bp.post('/auth/logout')
def logout():
    user = session["user"]
    if not user:
        return jsonify({"status": "error", "message": "Unauthorised Access."})
    
    session.clear()
    return render_template('login.html')