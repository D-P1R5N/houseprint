from houseprint import db
from datetime import datetime
import json

class Ingredient(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    uuid = db.Column(db.String(), nullable=False, unique=True)
    #serves = db.Column(db.Integer, nullable=True)
    #category = db.Column(db.String(), nullable=True)
    #special = db.Column(db.String(), nullable=True)

class XrefRecipeIngredient(db.Model):
    __tablename__ = "xref"
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.id'), nullable=False)
