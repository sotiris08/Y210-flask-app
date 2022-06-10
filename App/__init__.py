from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ['SECRET_KEY']
app.config["WTF_CSRF_SECRET_KEY"] = os.environ['WTF_CSRF_SECRET_KEY']

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = os.environ['OAUTHLIB_INSECURE_TRANSPORT']

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from App import routes
from App.User import User

@login_manager.user_loader
def load_user(uuid):
    user = User()
    user.getUserById(uuid)
    return user