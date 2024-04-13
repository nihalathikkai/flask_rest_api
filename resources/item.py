from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, schema=ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @jwt_required()
    @blp.arguments(schema=ItemSchema)
    @blp.response(201, schema=ItemSchema)
    def post(self, request_data):
        item = ItemModel(**request_data)

        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(409, message="Item already exits for the store.")
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item.")

        return item


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, schema=ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    @blp.arguments(schema=ItemUpdateSchema)
    @blp.response(200, schema=ItemSchema)
    def put(self, request_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            if "name" in request_data:
                item.name = request_data["name"]
            if "price" in request_data:
                item.price = request_data["price"]
        else:
            item = ItemModel(id=item_id, **request_data)

        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(409, message="Item already exits for the store.")
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item.")

        return item

    @jwt_required(fresh=True)
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)

        try:
            db.session.delete(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while deleting the item.")

        return {"message": "Item deleted."}, 200
