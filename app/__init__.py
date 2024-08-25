from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
admin = Admin(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)

# page user will be directed to if not logged-in and route is @login_required
login.login_view = "login"

from app import admin_page, models, routes
