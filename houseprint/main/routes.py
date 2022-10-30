from flask import render_template, url_for, flash, redirect, request, jsonify, Blueprint
from houseprint import app, db, bcrypt
from houseprint.users.models import User
from flask_login import login_required

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
@main.route("/home", methods=["GET", "POST"])
def home():
    return render_template("index.html", _title="Housemates")


@main.route("/screen", methods=["GET","POST"])
@login_required
def screen():
    return render_template("screen.html")
