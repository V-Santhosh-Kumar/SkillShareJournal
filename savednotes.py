from models import SavedNotes, User, Note
from flask import request, jsonify, Blueprint


savednotes_bp = Blueprint('savednotes_bp', __name__)

@savednotes_bp.post("/savedNotes/new")
def addsavednotes():
    try:

        data = request.get_json()
        # userId = data.get("userId")
        notesId = data.get("notesId")

        # if not userId: 
        #     return jsonify({"status": "error", "message": "userId is Required."})
        
        if not notesId: 
            return jsonify({"status": "error", "message": "notesId is Required."})

        # user = User.objects(id=userId).first()
        # if not user:
        #     return jsonify({"status": "error", "message": "User not found."})
        
        note = Note.objects(id=notesId).first()
        if not note:
            return jsonify({"status": "error", "message": "Note not found."})
        
        SavedNotes(
            # user = user,
            note = note
        ).save()


        return jsonify({"status": "success", "message": "SavedNotes Added Successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

@savednotes_bp.get("/savednotes/getAll")
def getAllSavedNotes():
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

@savednotes_bp.get('/savednotes/getSpecific')
def getSpecificSavedNotes():
    try:
        id = request.args.get('id')

        if not id:
            return jsonify({"status": "error", "message": "Id is Required"})

        savedNotes = SavedNotes.objects(id=id).first()

        if not savedNotes:
            return jsonify({"status": "error", "message": "SavedNotes not found."})

        data = { 
            "id": savedNotes.id,
            "user": savedNotes.user.name,
            "notes": savedNotes.note.name,
            "addedTime": savedNotes.addedTime,
            "updatedTime": savedNotes.updatedTime
        }   

        return jsonify({"status": "success", "message": "Role Retrieved Successfully", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  

@savednotes_bp.put('/savedNotes/update')
def updatdSavedNotes():
    try:
        id = request.args.get('id')

        if not id:
            return jsonify({"status": "error", "message": "Id is Required"})

        savedNotes = SavedNotes.objects(id=id).first()

        if not savedNotes:
            return jsonify({"status": "error", "message": "SavedNotes not found."})
        
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
        

        savedNotes.user = user
        savedNotes.note = note
        
        savedNotes.save()

        return jsonify({"status": "success", "message": "SavedNotes updated Successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  

@savednotes_bp.put('/savedNotes/delete')
def deleteSavedNotes():
    try:
        id = request.args.get('id')

        if not id:
            return jsonify({"status": "error", "message": "Id is Required"})

        savedNotes = SavedNotes.objects(id=id).first()

        if not savedNotes:
            return jsonify({"status": "error", "message": "SavedNotes not found."})
        
        savedNotes.delete()

        return jsonify({"status": "success", "message": "SavedNotes updated Successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  
