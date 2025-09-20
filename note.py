from mongoengine import *
from models import *
from flask import request, jsonify, Blueprint


note_bp = Blueprint('note_bp', __name__)

@note_bp.post("/note/new")
def addNote():
    try:
        title = request.form.get("title")
        description = request.form.get("description")
        code = request.form.get("code")
        tag = request.form.get("tag")
        images = request.files.getlist("images[]")  # receive multiple files

        if not title or not description:
            return jsonify({"status": "error", "message": "All Fields are Required"})

        # Save images (example: local 'uploads/' folder)
        saved_files = []
        for img in images:
            if img.filename:
                filepath = f"static/uploads/{img.filename}"
                img.save(filepath)
                saved_files.append(filepath)

        note = Note(
            title=title,
            description=description,
            code=code,
            tag=tag,
            image=saved_files  # or store paths/URLs
        )
        note.save()

        return jsonify({"status": "success", "message": "Note Added Successfully"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})



@note_bp.get("/note/getAll")
def get_all_notes():
    try:
        notes = Note.objects()
        note_list = []
        
        for note in notes:
            isLiked = Like.objects(note=note).first() is not None
            isSaved = SavedNotes.objects(note=note.id).first() is not None
            likeCount = Like.objects().count()
            data = {
                "id": note.id,
                "title": note.title,
                "description": note.description,
                "code": note.code,
                "image": note.image,
                "tag": note.tag.name if note.tag else None,
                "user": note.user.username if note.user else None,
                "addedTime": note.addedTime,
                "updatedTime": note.updatedTime,
                "isSaved": isSaved,
                "isLiked": isLiked,
                "likeCount": likeCount
            }
            note_list.append(data)

        return jsonify({"status": "success", "message": "Notes Retrieved Successfully", "data": note_list})
    
    except Exception as e:
        
        return jsonify({"status": "error", "message": str(e)})
    

@note_bp.get('/note/getSpecific')
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
                "tag": note.tag,
                "user": note.user.name,
                "addedTime": note.addedTime,
                "updatedTime": note.updatedTime
            }
        
        return jsonify({"status": "success", "message": "Note Retrieved Successfully", "data": data})
    
    except Exception as e:

        return jsonify({"status": "error", "message": str(e)})


@note_bp.put('/note/update')
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
        note.tag = data.get("tag")

        note.save()

        return jsonify({"status": "success", "message": "Note Updated Successfully"})
    
    except Exception as e:

        return jsonify({"status": "error", "message": str(e)})
    
@note_bp.put('/note/delete')
def deleteNote():
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
    

