import uuid

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, schema=ItemSchema(many=True))
    def get(self):
        return items.values()

    @blp.arguments(schema=ItemSchema)
    @blp.response(201, schema=ItemSchema)
    def post(self, request_data):
        if request_data["store_id"] not in stores:
            abort(404, message="Store not found.")

        for item in items.values():
            if (
                request_data["name"] == item["name"]
                and request_data["store_id"] == item["store_id"]
            ):
                abort(400, message="Item already exists.")

        while True:
            item_id = uuid.uuid4().hex
            if item_id not in items:
                break

        item_data = {
            "id": item_id,
            "store_id": request_data["store_id"],
            "name": request_data["name"],
            "price": request_data["price"],
        }
        items[item_id] = item_data

        return item_data, 201


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, schema=ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(schema=ItemUpdateSchema)
    @blp.response(200, schema=ItemSchema)
    def put(self, request_data, item_id):
        try:
            items[item_id] |= request_data
            # if "name" in request_data:
            #     items[item_id]["name"] = request_data["name"]
            # if "price" in request_data:
            #     items[item_id]["price"] = request_data["price"]
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")
