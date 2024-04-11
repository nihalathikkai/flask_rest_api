from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import StoreModel
from schemas import StoreSchema


blp = Blueprint("stores", __name__, description="Operations on store")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, schema=StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(schema=StoreSchema)
    @blp.response(201, schema=StoreSchema)
    def post(self, request_data):
        store = StoreModel(**request_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(409, message=f"Store '{store.name}' already exits.")
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the store.")

        return store


@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, schema=StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        try:
            db.session.delete(store)
            db.session.commit()
        except SQLAlchemyError as e:
            print(e)
            abort(500, message="An error occured while deleting the store.")

        return {"message": "Store deleted."}, 200
