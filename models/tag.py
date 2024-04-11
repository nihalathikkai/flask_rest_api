from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)

    store = db.relationship("StoreModel", back_populates="tags")
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")

    __table_args__ = (db.UniqueConstraint("name", "store_id"),)


class ItemsTags(db.Model):
    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), unique=False, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), unique=False, nullable=False)

    __table_args__ = (db.UniqueConstraint("item_id", "tag_id"),)
