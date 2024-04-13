from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import StoreModel, TagModel, ItemModel
from schemas import TagSchema, TagsAndItemsSchema


blp = Blueprint("tags", __name__, description="Operations on tags")


@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @jwt_required()
    @blp.response(200, schema=TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store.tags.all()

    @jwt_required()
    @blp.arguments(schema=TagSchema)
    @blp.response(201, schema=TagSchema)
    def post(self, request_data, store_id):
        tag = TagModel(**request_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            abort(409, message="Tag already exists")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occured while fetching tags.: {e}")

        return tag


@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItems(MethodView):
    @jwt_required()
    @blp.response(201, schema=TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        if item.store_id != tag.store_id:
            abort(400, message="Item and tag does not belong to same store.")

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(409, message="Item already has the tag.")
        except SQLAlchemyError as e:
            abort(500, message=f"An error occured while adding the tag.: {e}")

        return tag

    @jwt_required(fresh=True)
    @blp.response(200, schema=TagsAndItemsSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id, description="Item not found.")
        tag = TagModel.query.get_or_404(tag_id, description="Tag not found.")

        if item.store_id != tag.store_id:
            abort(400, message="Item and tag does not belong to same store.")

        if tag not in item.tags:
            abort(400, message="Tag not assignd to item.")

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while adding the tag.")

        return {"message": "Tag removed from item", "item": item, "tag": tag}


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, schema=TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        return tag

    @blp.response(
        202,
        description="Deletes a tag if no item is tagged with it",
        example={"message": "Tag Deleted"},
    )
    @blp.alt_response(400, description="Returned if tag is assigned one ore more items.")
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        if tag.items:
            abort(400, message="Could not delete tag in use.")

        try:
            db.session.delete(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"An error occured while deleting the item.: {e}")

        return {"message": "Item deleted."}
