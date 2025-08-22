from models import Role
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.post("/role/new")
def addRole():
    try:

        data = request.get_json()
        name = data.get("name") 

        if not name:
            return jsonify({"status": "error", "message": "All Fields are Required"})
        
        Role( 
            name = name
        ).save()


        return jsonify({"status": "success", "message": "Role Added Successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

@app.get("/role/getAll")
def getAllRole():
    try:

        roles = Role.objects()

        roleList = []

        for role in roles:
            data = { 
                "id": role.id,
                "name": role.name,
                "addedTime": role.addedTime,
                "updatedTime": role.updatedTime
            }   

            roleList.append(data)
        
        return jsonify({"status": "success", "message": "Roles Retrieved Successfully", "data": roleList})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  
         

    