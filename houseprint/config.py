import os
from secrets import token_hex

class Config:
    SECRET_KEY = os.environ.get("HOUSEPRINT_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///houseprint.db'

    ALLOWED_EXTENSIONS = {'png','jpg','csv','json'}
    TEMPLATES_AUTO_RELOAD = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.environ.get("EMAIL_ADDR")
    MAIL_PASSWORD = os.environ.get("EMAIL_APP_PASS")
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
