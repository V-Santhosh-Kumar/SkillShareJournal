from models import Tags
from flask import request, jsonify, Blueprint


tags_bp = Blueprint('tags_bp', __name__)


@tags_bp.post("/tags/new")
def addtags():
    try:

        data = request.get_json()
        name = data.get("name")
        description = data.get("description")

        if not name or description:
            return jsonify({"status": "error", "message": "All Fields are Required"})
        
        Tags(
            name = name,
            description = description
        ).save()


        return jsonify({"status": "success", "message": "Tags Added Successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

@tags_bp.get("/tags/getAll")
def getAllTags():
    try:

        tags = Tags.objects()

        tagsList = []

        for tag in tags:
            data = {
                "id": tag.id,
                "name": tag.name,
                "description": tag.description,
                "addedTime": tag.addedTime,
                "updatedTime": tag.updatedTime
            }

            tagsList.append(data)

        return jsonify({"status": "success", "message": "Tags Retrieved Successfully", "data": tagsList})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  

@tags_bp.get('/tags/getSpecific')
def getSpecificTags():
    try:
        id = request.args.get('id')

        if not id:
                return jsonify({"status": "error", "message": "Id is Required"})

        tag = Tags.objects(id=id).first()
        
        if not tag:
                return jsonify({"status": "error", "message": "Tag not found."})

        data = { 
                "id": tag.id,
                "name": tag.name,
                "description": tag.description,
                "addedTime": tag.addedTime,
                "updatedTime": tag.updatedTime
        }   

        return jsonify({"status": "success", "message": "Role Retrieved Successfully", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  

@tags_bp.put('/tag/update')
def updateTags():
     try:
        id = request.args.get('id')     

        if not id:
             return jsonify({"status": "error", "message": "Id is Required"})
        
        tag = Tags.object(id=id).first()

        if not tag:
             return jsonify({"status": "error", "message": "Tag not found"})
        
        data = request.get_json()


        tag.name = data.get("name")
        tag.description = data.get("description")
        tag.save()

        return jsonify({"status": "success", "message": "Tag updated Successfully"})
     except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  


@tags_bp.put('/tags/delete')
def deleteTags():
    try:
        id = request.args.get('id')

        if not id:
            return jsonify({"status": "error", "message": "Tags is Required"})

        tags = Tags.objects(id=id).first()

        if not tags:
            return jsonify({"status": "error", "message": "Tags not found."})
        
        tags.delete()

        return jsonify({"status": "success", "message": "Tags updated Successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  