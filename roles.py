from models import Role
from flask import request, jsonify
from app import app

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
         

@app.get('/role/getSpecific')
def getSpecificRole():
    try:
        id = request.args.get('id')

        if not id:
            return jsonify({"status": "error", "message": "Id is Required"})

        role = Role.objects(id=id).first()

        if not role:
            return jsonify({"status": "error", "message": "Role not found."})

        data = { 
            "id": role.id,
            "name": role.name,
            "addedTime": role.addedTime,
            "updatedTime": role.updatedTime
        }   

        return jsonify({"status": "success", "message": "Role Retrieved Successfully", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  

@app.put('/role/update')
def updateRole():
    try:
        id = request.args.get('id')

        if not id:
            return jsonify({"status": "error", "message": "Id is Required"})

        role = Role.objects(id=id).first()

        if not role:
            return jsonify({"status": "error", "message": "Role not found."})
        
        data = request.get_json()


        role.name = data.get("name")
        role.save()

        return jsonify({"status": "success", "message": "Role updated Successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  
    


@app.put('/role/delete')
def updateRole():
    try:
        id = request.args.get('id')

        if not id:
            return jsonify({"status": "error", "message": "Id is Required"})

        role = Role.objects(id=id).first()

        if not role:
            return jsonify({"status": "error", "message": "Role not found."})
        
        role.delete()

        return jsonify({"status": "success", "message": "Role updated Successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  