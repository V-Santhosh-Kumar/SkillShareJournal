from models import Like, User, Note
from flask import request, jsonify, Blueprint


like_bp = Blueprint('like_bp', __name__)

@like_bp.post("/like/liked")
def addLike():
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
        
        like = Like.objects(note=note).first()

        if like:
            like.count += 1
            like.save()
        else:
            Like(
                user = user,
                note = note,
                count = 1
            ).save()


        return jsonify({"status": "success", "message": "Liked Successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

@like_bp.post("/like/disliked")
def removeLike():
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
        
        like = Like.objects(note=note).first()

        if like:
            like.count -= 1
            like.save()
            
        return jsonify({"status": "success", "message": "Liked Successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

