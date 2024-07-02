from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200


######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data), 200


######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((p for p in data if p["id"] == id), None)
    if picture:
        return jsonify(picture), 200

    return {"message": "Picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    picture = request.get_json()
    if not picture:
        return {"message": "No input data provided"}, 400

    id = picture.get("id")
    if not id:
        return {"message": "No id provided"}, 400

    if next((p for p in data if p["id"] == id), None):
        return {"message": f"picture with id {id} already present"}, 302

    data.append(picture)
    return jsonify(picture), 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.get_json()
    if not picture:
        return {"message": "No input data provided"}, 400

    if picture["id"] != id:
        return {"message": "id in URL does not match id in data"}, 400

    picture = next((p for p in data if p["id"] == id), None)
    if not picture:
        return {"message": "Picture not found"}, 404

    picture.update(picture)
    return jsonify(picture), 200


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    picture = next((p for p in data if p["id"] == id), None)
    if not picture:
        return {"message": "Picture not found"}, 404

    data.remove(picture)
    return make_response("", 204)
