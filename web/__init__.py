from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_socketio import SocketIO

website = Flask(__name__)
website.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
website.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///holic.db'
socketio=SocketIO(website)

db = SQLAlchemy(website)
bcrypt = Bcrypt(website)

login_manager = LoginManager(website)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'



from web import routes