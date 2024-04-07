import uuid

from flask import request

# from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores

blp = Blueprint("stores", __name__, description="Operations on store")


@blp.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


@blp.post("/store")
def create_store():
    request_data = request.get_json()

    if "name" not in request_data:
        abort(400, message="Bad Request, Ensure payload contains 'name'")

    for store in stores.values():
        if request_data["name"] == store["name"]:
            abort(400, message="Store already exists.")

    while True:
        store_id = uuid.uuid4().hex
        if store_id not in stores:
            break

    store_data = {
        "id": store_id,
        "name": request_data["name"],
        # "items": [],
    }
    stores[store_id] = store_data

    return store_data, 201


@blp.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")
        # return {"message": "Store not found."}, 404


@blp.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not found.")
        # return {"message": "Store not found."}, 404
