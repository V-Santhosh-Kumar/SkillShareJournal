from models import SavedNotes, User, Note, Like, Comment
from flask import request, jsonify, Blueprint, session


savednotes_bp = Blueprint('savednotes_bp', __name__)

@savednotes_bp.post("/savedNotes/toggle")
def addsavednotes():
    try:

        data = request.get_json()
        notesId = data.get("notesId")

        user = session.get("user")
        userId = user.get('id')

        if not userId: 
            return jsonify({"status": "error", "message": "userId is Required."})
        
        if not notesId: 
            return jsonify({"status": "error", "message": "notesId is Required."})
        
        saved = SavedNotes.objects(note=notesId).first()

        if saved:
            saved.delete()
            return jsonify({"status": "success", "action": "unsaved"})
        else:        
            note = Note.objects(id=notesId).first()
            if not note:
                return jsonify({"status": "error", "message": "Note not found."})
        
            SavedNotes(
                # user = user,
                note = note
            ).save()


            return jsonify({"status": "success", "action": "saved"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

@savednotes_bp.get("/savedNotes/getAll")
def getSavedNotes():
    try:
        user = session.get("user")
        user_id = user.get("id") if user else None

        if not user_id:
            return jsonify({
                "status": "error",
                "message": "User not logged in. Please log in to continue."
            }), 401

        saved = SavedNotes.objects()  # or filter your relation
        note_ids = [s.note.id for s in saved]

        notes = Note.objects(id__in=note_ids)
        data = []
        for note in notes:
            isLiked = Like.objects(note=note).first() is not None
            isSaved = SavedNotes.objects(note=note.id).first() is not None
            likeCount = Like.objects().count()

            comments = Comment.objects(note=note).order_by("-addedTime")
            comment_list = []
            for c in comments:
                comment_list.append({
                    "id": str(c.id),
                    "user": c.user.username if c.user else None,
                    "comment": c.comment,
                    "addedTime": c.addedTime,
                    "updatedTime": c.updatedTime
                })

            data.append({
                "id": str(note.id),
                "title": note.title,
                "description": note.description,
                "image": note.image,
                "tag": note.tag.name if note.tag else None,
                "user": note.user.username if note.user else None,
                "addedTime": note.addedTime,
                "updatedTime": note.updatedTime,
                "isSaved": isSaved,
                "isLiked": isLiked,
                "likeCount": likeCount,
                "comments": comment_list
            })

        return jsonify({"status": "success", "data": data})
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

        user = session.get("user")
        userId = user.get('id')

        if not userId: 
            return jsonify({"status": "error", "message": "userId is Required."})
        
        notesId = data.get("notesId")    
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
