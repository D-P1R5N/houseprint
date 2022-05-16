from datetime import datetime
from houseprint import db
import json

class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)

    def __repr__(self):
        return f"ID: {self.id}\nName:{self.name}"

class Item(db.Model):
    __tablename__ = "item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    barcode = db.Column(db.String(), nullable=False, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    _category = db.relationship('Category', backref='category')

    def __repr__(self):
        return f"{self.name}\n{self.barcode}\n{self._category.name}"

    def payload(self):
        return {
            "id":self.id,
            "name":self.name,
            "barcode":self.barcode,
            "category":self._category.name
        }

class Inventory(db.Model):
    __tablename__= 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    _item = db.relationship('Item', backref='item', lazy=True)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"{self.id}:{self._item.name}\nInStock:{self.quantity}"

    def payload(self):
        return {
            "id": self.id,
            "name": self._item.name,
            "quantity": self.quantity,
            "barcode": self._item.barcode,
            "category": self._item._category.name
        }
