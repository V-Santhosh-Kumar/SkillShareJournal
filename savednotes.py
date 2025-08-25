from models import SavedNotes
from flask import Flask, request,jsonify

app =Flask(__name__)

@app.post("/savedNotes/new")
def addsavednotes():
    try:

        data = request.get_json
        user = data.get("user")

        data = request.get_json
        notes = data.get("notes")

        if not user or notes:
            return jsonify({"status": "error", "message": "All Fields are Required"})
        
        SavedNotes(
            user = user,
            notes= notes
        ).save()


        return jsonify({"status": "success", "message": "SavedNotes Added Successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

@app.get("/savednotes/getAll")
def getAllTags():
    try:

        SavedNotes = SavedNotes.objects()

        SavedNotes = []

        for SavedNotes in SavedNotes:
            data = {
                "id": SavedNotes.id,
                "user": SavedNotes.name,
                "notes": SavedNotes.description,
                "addedTime": SavedNotes.addedTime,
                "updatedTime": SavedNotes.updatedTime
            }

            SavedNotes.append(data)

        return jsonify({"status": "success", "message": "SavedNotes Retrieved Successfully", "data": SavedNotes})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  

