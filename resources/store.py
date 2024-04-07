import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores
from schemas import StoreSchema


blp = Blueprint("stores", __name__, description="Operations on store")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, schema=StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(schema=StoreSchema)
    @blp.response(200, schema=StoreSchema)
    def post(self, request_data):
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


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, schema=StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="Store not found.")

    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found.")
