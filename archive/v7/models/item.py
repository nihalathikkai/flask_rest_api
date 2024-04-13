from db import db

# from sqlalchemy import Column, Integer, String, Float


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)

    store = db.relationship("StoreModel", back_populates="items")
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")

    __table_args__ = (db.UniqueConstraint("name", "store_id"),)

    # id = Column(Integer, primary_key=True)
    # name = Column(String(80), unique=False, nullable=False)
    # price = Column(Float(precision=2), unique=False, nullable=False)
    # store_id = Column(Integer, unique=Flase, nullable=False)
