from models import SavedNotes, User, Note
from flask import Flask, request,jsonify

app =Flask(__name__)

@app.post("/savedNotes/new")
def addsavednotes():
    try:

        data = request.get_json()
        userId = data.get("userId")
        notesId = data.get("notesId")

        if not userId: 
            return jsonify({"status": "error", "message": "userId is Required."})
        
        if not notesId: 
            return jsonify({"status": "error", "message": "notesId is Required."})

        user = User.objects(id=userId).first()
        if not user:
            return jsonify({"status": "error", "message": "User not found."})
        
        note = Note.objects(id=notesId).first()
        if not note:
            return jsonify({"status": "error", "message": "Note not found."})
        
        SavedNotes(
            user = user,
            note = note
        ).save()


        return jsonify({"status": "success", "message": "SavedNotes Added Successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

@app.get("/savednotes/getAll")
def getAllTags():
    try:

        savedNotes = SavedNotes.objects()

        savedNotesList = []

        for savednote in savedNotes:
            data = {
                "id": savednote.id,
                "user": savednote.user.name,
                "notes": savednote.note.name,
                "addedTime": savednote.addedTime,
                "updatedTime": savednote.updatedTime
            }

            savedNotesList.append(data)

        return jsonify({"status": "success", "message": "SavedNotes Retrieved Successfully", "data": savedNotesList})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  

