from models import Tags
from flask import Flask, request,jsonify

app = Flask(__name__)

@app.post("/tags/new")
def addtags():
    try:

        data = request.get_json()
        name = data.get("name")

        data = request.get_json()
        descrption = data.get("description")

        if not name or descrption:
            return jsonify({"status": "error", "message": "All Fields are Required"})
        
        Tags(
            name = name,
            description = descrption
        ).save()


        return jsonify({"status": "success", "message": "Tags Added Successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    

@app.get("/tags/getAll")
def getAllTags():
    try:

        tags = Tags.objects()

        tagsList = []

        for tags in tags:
            data = {
                "id": tags.id,
                "name": tags.name,
                "description": tags.description,
                "addedTime": tags.addedTime,
                "updatedTime": tags.updatedTime
            }

            tagsList.append(data)

        return jsonify({"status": "success", "message": "Tags Retrieved Successfully", "data": tagsList})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})  
                 