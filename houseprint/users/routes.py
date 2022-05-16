from flask import render_template, url_for, flash, redirect, request, jsonify, abort, Blueprint
from flask_login import current_user, login_required, login_user, logout_user

from functools import wraps

from houseprint import db, app, bcrypt
from houseprint.users.forms import (LoginForm, RegistrationForm,
    ResetRequestForm, ResetPasswordForm)
from houseprint.users.models import User

user = Blueprint('user', __name__)
"""
The following method is a template for checking a potential users IP address
against trust IP addresses in a seperate database. This database will also
be used to check a user's permissions.
-DB
--Table: AnonApproved {
    id: PK
    user_id: FK U (reference to table)
    ip_addr: U (hashed)
}
--Table: AnonDenied {
    id: PK
    ip_addr: U (hashed)
}
--Table: Users {
    id: PK
    u_id: FK U(refers to seperate db)
}
--Table: Permissions {
    id: PK
    u_id: FK U (refers to table)
    rule_id: U (points to json file, static files)
}
"""
#def check_ip_addr():
#    @wraps(app.before_request)
#
#    def _check_ip_addr(*args, **kwargs):
#        ip_addr = request.environ.get('REMOTE_ADDR', request.remote_addr)
#        if AnonApproved.query.filter_by(ip_addr=bcrypt.check_password_hash(ip_addr)).first():
#            flash(f"{ip_addr} approved! Welcome.")
#            return
#        else:
#            abort(404)


@user.route("/user/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login unsuccessful, check credentials.", 'danger')
    return render_template("login.html", form = form)

@user.route('/user/register', methods = ["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You may now login.', 'success')
        return render_template(url_for("user.login"))
    return render_template('register.html', form=form)

@user.route("/user/reset_password")
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #INSERT CODE TO SEND EMAIL

        #INSERT CODE TO SEND EMAIL
        flash("An email has been sent with the reset instructions.", 'info')
        return redirect(url_for('user.login'))
    return render_template('reset_request.html', form=form)

@user.route('/user/reset_password/<token>', methods = ["GET", "POST"])
def reset_token():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash("Token is invalid or expired.", 'warning')
        return redirect(url_for('user.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash("Password updated successfully.", 'success')
        return redirect(url_for('user.login'))
    return render_template('reset_token.html', form=form)

@user.route('/user/logout', methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for('main.home'))
