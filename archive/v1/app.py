import uuid

from flask import Flask, request, 

from flask_smorest import abort

from db import items, stores

app = Flask(__name__)


@app.get("/")
def root():
    return {"message": "I am live!!!"}


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    request_data = request.get_json()

    if "name" not in request_data:
        abort(400, message="Bad Request, Ensure payload contains 'name'")

    for store in stores.values():
        if request_data["name"] == store["name"]:
            # abort(400, message="Store already exists.")

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


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found.")
        # return {"message": "Store not found."}, 404


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not found.")
        # return {"message": "Store not found."}, 404


@app.get("/item")
def get_items():
    return {"items": list(items.values())}


@app.post("/item")
def create_item():
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
        # return {"message": "Store not found."}, 404

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


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Item not found.")
        # return {"message": "Item not found."}, 404


@app.put("/item/<string:item_id>")
def update_item(item_id):
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


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found.")
