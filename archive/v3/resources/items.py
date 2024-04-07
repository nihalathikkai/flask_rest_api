import uuid

from flask import request

from flask.views import MethodView
from flask_smorest import Blueprint, abort

from db import stores, items

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        request_data = request.get_json()

        if (
            "store_id" not in request_data
            or "name" not in request_data
            or "price" not in request_data
        ):
            abort(
                400,
                message="Bad Request, Ensure payload contains 'store_id', 'name' and 'price'",
            )

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
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def put(self, item_id):
        request_data = request.get_json()

        if "name" not in request_data and "price" not in request_data:
            abort(
                400,
                message="Bad Request, Ensure payload contains 'name' or 'price'",
            )

        try:
            # items[item_id] |= request_data
            if "name" in request_data:
                items[item_id]["name"] = request_data["name"]
            if "price" in request_data:
                items[item_id]["price"] = request_data["price"]
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")
