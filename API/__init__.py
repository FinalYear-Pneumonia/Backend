from flask import Flask
from API.extensions import database, bcrypt, jwt, mail, cors, migrate
from flask_restx import Api
from dotenv import load_dotenv
from API.users.controllers import user_ns
from API.main.routes import hms_ns



load_dotenv()

def create_application(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    api = Api(app, docs='\docs')
    
    database.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    migrate.init_app(app, database)

    api.add_namespace(user_ns)
    api.add_namespace(hms_ns)
    

    with app.app_context():
        database.drop_all()
        database.create_all()
        

    return app