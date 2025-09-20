from models import Comment, User, Note
from flask import request, jsonify, Blueprint


comment_bp = Blueprint('comment_bp', __name__)

@comment_bp.post("/comment/new")
def addComment():
    try:

        data = request.get_json()
        comment = data.get("comment") 
        # userId = data.get("userId")
        notesId = data.get("notesId")

        if not comment:
            return jsonify({"status": "error", "message": "All Fields are Required"})

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

        comment = Comment( 
            comment = comment,
            # user = user,
            note = note,
        ).save()


        return jsonify(
            {"status": "success", "message": "Comment Added Successfully",
              "data":{
                  "id": str(comment.id),
                  "username":getattr(comment.user,"username","Anonymous"),
                  "comment": comment.comment} 
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

@comment_bp.get("/comment/getAll")
def getAllComment():
    try:

        comments = Comment.objects()

        commentList = []

        for comment in comments:
            data = { 
                "id": comment.id,
                "comment": comment.comment,
                "user":comment.user,
                "note":comment.note,
                "addedTime": comment.addedTime,
                "updatedTime": comment.updatedTime
            }   

            commentList.append(data)
        
        return jsonify({"status": "success", "message": "comments Retrieved Successfully", "data": commentList})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  
         

@comment_bp.get('/comment/getSpecific')
def getSpecificComment():
    try:
        id = request.args.get('id')

        if not id:
            return jsonify({"status": "error", "message": "Id is Required"})

        comment = Comment.objects(id=id).first()

        if not comment:
            return jsonify({"status": "error", "message": "comment not found."})

        data = { 
            "id": comment.id,
            "comment": comment.comment,
            "user":comment.user,
            "note":comment.note,
            "addedTime": comment.addedTime,
            "updatedTime": comment.updatedTime
        }   

        return jsonify({"status": "success", "message": "comment Retrieved Successfully", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  

@comment_bp.put('/comment/update')
def updateComment():
    try:
        id = request.args.get('id')

        if not id:
            return jsonify({"status": "error", "message": "Id is Required"})

        comment = Comment.objects(id=id).first()

        if not comment:
            return jsonify({"status": "error", "message": "Comment not found."})
        
        data = request.get_json()
        comment = data.get("comment") 
        userId = data.get("userId")
        notesId = data.get("notesId")

        if not comment:
            return jsonify({"status": "error", "message": "All Fields are Required"})

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


        comment.comment = comment

        comment.save()

        return jsonify({"status": "success", "message": "Comment updated Successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  
    


@comment_bp.put('/comment/delete')
def deleteComment():
    try:
        id = request.args.get('id')

        if not id:
            return jsonify({"status": "error", "message": "Id is Required"})

        comment = Comment.objects(id=id).first()

        if not comment:
            return jsonify({"status": "error", "message": "Comment not found."})
        
        comment.delete()

        return jsonify({"status": "success", "message": "Comment updated Successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  
    

@comment_bp.get("/comment/getByNoteId/<note_id>")
def getByNoteId(note_id):
    try:
        comments = Comment.objects(note=note_id).order_by("-addedTime")
        commentList = []

        for c in comments:
            commentList.append({
                "id": str(c.id),
                "username": getattr(c.user, "username", "Anonymous"),
                "comment": c.comment,
                "addedTime": c.addedTime
            })

        return jsonify({
            "status": "success",
            "message": "Comments Retrieved Successfully",
            "data": commentList
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
