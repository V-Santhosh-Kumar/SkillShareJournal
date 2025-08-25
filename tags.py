from models import Tags
from flask import Flask, request,jsonify

app = Flask(__name__)

@app.post("/tags/new")
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
    
    
@app.get("/tags/getAll")
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
                 