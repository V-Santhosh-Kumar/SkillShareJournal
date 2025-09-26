from mongoengine import *
from models import *
from flask import request, jsonify, Blueprint , url_for,session, render_template


note_bp = Blueprint('note_bp', __name__)

@note_bp.post("/note/new")
def addNote():
    try:
        title = request.form.get("title")
        description = request.form.get("description")
        code = request.form.get("code")
        tag = request.form.get("tag")
        images = request.files.getlist("images[]")  # receive multiple files

        user = session.get("user")
        print(user)
        userId = user.get('id')
        print(userId)


        user = User.objects(id=userId).first()
        if not user: 
            return jsonify({"status": "error", "message": "user is Required."})

        if not title or not description:
            return jsonify({"status": "error", "message": "All Fields are Required"})

        # Save images (example: local 'uploads/' folder)
        saved_files = []
        for img in images:
            if img.filename:
                filepath = f"static/uploads/{img.filename}"
                img.save(filepath)
                saved_files.append(filepath)
            
        shareable_link = str(uuid4())

        note = Note(
            title=title,
            description=description,
            code=code,
            tag=tag,
            image=saved_files,# or store paths/URLs
            shareableLink=shareable_link,
            user = user 
        )
        note.save()

        return jsonify({"status": "success", "message": "Note Added Successfully","shareableLink": f"/note/{shareable_link}"})
    
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
            likeCount = Like.objects(note=note).count()
            note_url = "/note/"+note.id



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
            data = {
                "id": note.id,
                "title": note.title,
                "description": note.description,
                "code": note.code,
                "image": note.image,
                "tag": note.tag.name if note.tag else None,
                "user": note.user.username if note.user else None,
                "shareableLink": note.shareableLink,
                "addedTime": note.addedTime,
                "updatedTime": note.updatedTime,
                "isSaved": isSaved,
                "isLiked": isLiked,
                "likeCount": likeCount,
                "link": note_url,
                "comments": comment_list
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
                "user": note.user.username if note.user else None,
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



@note_bp.get("/note/<id>")
def getNote(id):
    try:
        note = Note.objects(id=id).first()
        if not note:
            return jsonify({"status": "error", "message": "Note not found"})

        return render_template("noteDetail.html", note=note)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})




