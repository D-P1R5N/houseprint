from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
    IntegerField, RadioField, HiddenField, TextAreaField, SelectField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class Recipe(FlaskForm):



class Ingredient(FlaskForm):
    
