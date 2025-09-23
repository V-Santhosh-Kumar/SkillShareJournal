from models import Like, User, Note
from flask import request, jsonify, Blueprint


like_bp = Blueprint('like_bp', __name__)
from models import Like, Note
from flask import request, jsonify, Blueprint

like_bp = Blueprint('like_bp', __name__)

@like_bp.post("/like/toggle")
def toggleLike():
    try:
        data = request.get_json()
        notesId = data.get("notesId")

        if not notesId: 
            return jsonify({"status": "error", "message": "notesId is Required."})

        note = Note.objects(id=notesId).first()
        if not note:
            return jsonify({"status": "error", "message": "Note not found."})

        like = Like.objects(note=note).first()

        if like:
            # if already liked, unlike it
            like.delete()
            return jsonify({"status": "success", "action": "unliked"})
        else:
            Like(note=note, count=1).save()
            return jsonify({"status": "success", "action": "liked"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@like_bp.get("/likedNotes/getAll")
def getLikedNotes():
    try:
        # userId = request.args.get("userId")
        # if not userId:
        #     return jsonify({"status": "error", "message": "userId is required"})

        # get all liked notes for this user
        likes = Like.objects()
        note_ids = [l.note.id for l in likes]

        notes = Note.objects(id__in=note_ids)
        data = []
        for note in notes:
            data.append({
                "id": str(note.id),
                "title": note.title,
                "description": note.description,
                "image": note.image,
                "tag": note.tag.name if note.tag else None,
                "isSaved": False,   # you can also check SavedNotes model here
                "isLiked": True,    # since these are liked
                "likeCount": Like.objects(note=note.id).count()
            })

        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})