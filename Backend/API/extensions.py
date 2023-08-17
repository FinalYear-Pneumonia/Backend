from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from flask_migrate import Migrate
from flask_oauthlib.client import OAuth



database = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()
cors = CORS()
migrate = Migrate()
oauth = OAuth()
