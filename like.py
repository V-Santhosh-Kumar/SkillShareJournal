from models import Like, User, Note, Comment, SavedNotes
from flask import request, jsonify, Blueprint,session

like_bp = Blueprint('like_bp', __name__)

@like_bp.post("/like/toggle")
def toggleLike():
    try:
        user = session.get("user")
        user_id = user.get("id") if user else None

        if not user_id:
            return jsonify({
                "status": "error",
                "message": "User not logged in. Please log in to continue."
            }), 401

        data = request.get_json()
        notesId = data.get("notesId")

        if not notesId: 
            return jsonify({"status": "error", "message": "notesId is Required."})

        note = Note.objects(id=notesId).first()
        if not note:
            return jsonify({"status": "error", "message": "Note not found."})

        like = Like.objects(note=note, user=user).first()

        if like:
            # if already liked, unlike it
            like.delete()
            return jsonify({"status": "success", "action": "unliked"})
        else:
            Like(note=note, count=1, user=user).save()
            return jsonify({"status": "success", "action": "liked"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@like_bp.get("/likedNotes/getAll")
def getLikedNotes():
    try:
        user = session.get("user")
        user_id = user.get("id") if user else None

        if not user_id:
            return jsonify({
                "status": "error",
                "message": "User not logged in. Please log in to continue."
            }), 401

        # get all liked notes for this user
        likes = Like.objects()
        note_ids = [l.note.id for l in likes]

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
                "isSaved": isSaved,   # you can also check SavedNotes model here
                "isLiked": isLiked,    # since these are liked
                "likeCount": likeCount,
                "comments": comment_list
            })

        return jsonify({"status": "success", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})