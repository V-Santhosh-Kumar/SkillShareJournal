from models import Comment, User, Note
from flask import request, jsonify
from app import app

@app.post("/comment/new")
def addComment():
    try:

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

        comment = Comment( 
            comment = comment,
            user = user,
            note = note,
        ).save()


        return jsonify({"status": "success", "message": "Comment Added Successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

@app.get("/comment/getAll")
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
         

@app.get('/comment/getSpecific')
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

@app.put('/comment/update')
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
    


@app.put('/comment/delete')
def updateComment():
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