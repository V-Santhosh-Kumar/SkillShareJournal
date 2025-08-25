from mongoengine import *
from uuid import uuid4
from datetime import datetime
from models import Note
from flask import Flask, request, jsonify


app = Flask(__name__)

@app.post("/note/new")
def addNote():
    try:
        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        code = data.get("code")
        image = data.get("image")

        if not title or not description:
            return jsonify({"status": "error", "message": "All Fields are Required"})

        note = Note(title=title, description=description, code=code, image=image)
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
                "addedTime": note.addedTime,
                "updatedTime": note.updatedTime
            }
            note_list.append(data)

        return jsonify({"status": "success", "message": "Notes Retrieved Successfully", "data": note_list})
    
    except Exception as e:
        
        return jsonify({"status": "error", "message": str(e)})