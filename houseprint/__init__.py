from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from houseprint.config import Config

app = Flask(__name__)
db = SQLAlchemy()
csrf = CSRFProtect()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.home'
login_manager.login_message_category = 'info'
mail = Mail()

def create(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    csrf.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    mail.init_app(app)

    with app.app_context():
        from houseprint.users.models import User
        from houseprint.inventory.models import Item, Inventory, Category
        db.create_all()
        if not User.query.count() > 0:
            db.session.commit()

    from houseprint.users.routes import user
    from houseprint.main.routes import main
    from houseprint.inventory.routes import inv
    app.register_blueprint(user)
    app.register_blueprint(main)
    app.register_blueprint(inv)
    return app
