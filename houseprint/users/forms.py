from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
    IntegerField, RadioField, HiddenField, TextAreaField, SelectField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from houseprint.users.models import User
import string

class RegistrationForm(FlaskForm):
    username = StringField("Username",
        validators = [DataRequired(), Length(min=6, max=20)])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password",
        validators = [DataRequired(), Length(min=8, max=22)])
    confirm_password = PasswordField("Confirm Password",
        validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is already registered.")
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is already registered.")

    def password_security(self, password):
        _pass = set(password.data)
        if not all(
            tuple(
                map(
                    lambda x : any(_pass & set(x)),
                        [string.punctuation,
                        string.ascii_lowercase,
                        string.ascii_uppercase,
                        string.digits]
                    )
                )
            ):
            raise ValidationError("Password fails to meet security standards.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class ResetRequestForm(FlaskForm):
    #sends reset email to address
    email = StringField("Email", validators = [DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("Email not registered.")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators = [DataRequired()])
    confirm_password = PasswordField("Confirm Password",
        validators = [DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")
