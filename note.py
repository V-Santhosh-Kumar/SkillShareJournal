from mongoengine import *
from models import *
from flask import request, jsonify
from app import app

@app.post("/note/new")
def addNote():
    try:
        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        code = data.get("code")
        image = data.get("image")
        user_id = data.get("user_id")

        if not title or not description:
            return jsonify({"status": "error", "message": "All Fields are Required"})
        
        if not user_id:
            return jsonify({"status": "error", "message": "User Id not found"})
        
        user = User.objects(id=user_id).first()
        if not user:
            return jsonify({"status": "error", "message": "Invalid User"})

        note = Note(title=title, description=description, code=code, image=image, user=user)
        note.save()


        return jsonify({"status": "success", "message": "Note Added Successfully"})
    
    except Exception as e:

        return jsonify({"status": "error", "message": str(e)})


@app.get("/note/getAll")
def get_all_notes():
    try:
        notes = Note.objects()
        note_list = []
        
        for note in notes:
            data = {
                "id": note.id,
                "title": note.title,
                "description": note.description,
                "code": note.code,
                "image": note.image,
                "user": note.user.name,
                "addedTime": note.addedTime,
                "updatedTime": note.updatedTime
            }
            note_list.append(data)

        return jsonify({"status": "success", "message": "Notes Retrieved Successfully", "data": note_list})
    
    except Exception as e:
        
        return jsonify({"status": "error", "message": str(e)})
    

@app.get('/note/getSpecific')
def getSpecificNote():
    try:
        id = request.args.get('id')

        if not id:
            return jsonify({"status": "error", "message": "Id is Required"})

        note = Note.objects(id=id).first()

        if not note:
            return jsonify({"status": "error", "message": "Role not found."})

        data = {
                "id": note.id,
                "title": note.title,
                "description": note.description,
                "code": note.code,
                "image": note.image,
                "user": note.user.name,
                "addedTime": note.addedTime,
                "updatedTime": note.updatedTime
            }
        
        return jsonify({"status": "success", "message": "Note Retrieved Successfully", "data": data})
    
    except Exception as e:

        return jsonify({"status": "error", "message": str(e)})


@app.put('/note/update')
def updateNote():
    try:
        id = request.args.get('id')

        if not id:
            return jsonify({"status": "error", "message": "Id is Required"})
        
        note = Note.objects(id=id).first()

        if not note:
            return jsonify({"status": "error", "message": "Role not found."})
        
        data = request.get_json()

        note.title = data.get("title")
        note.description = data.get("description")
        note.code = data.get("code")
        note.image = data.get("image")

        note.save()

        return jsonify({"status": "success", "message": "Note Updated Successfully"})
    
    except Exception as e:

        return jsonify({"status": "error", "message": str(e)})
    
@app.put('/note/delete')
def updateNote():
    try:
        id = request.args.get('id')

        if not id:
            return jsonify({"status": "error", "message": "Id is Required"})

        note = Note.objects(id=id).first()

        if not note:
            return jsonify({"status": "error", "message": "Note not found."})
        
        note.delete()

        return jsonify({"status": "success", "message": "Note Deleted Successfully"})
    
    except Exception as e:

        return jsonify({"status": "error", "message": str(e)})  