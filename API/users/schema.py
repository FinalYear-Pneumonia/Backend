from flask_restx import fields
from API.users.controllers import user_ns

UserNewLoad = user_ns.model(
    "SignUp_Request Model",
    {
        "email": fields.String(),
        "username": fields.String(),
        "password": fields.String(),
        "confirm-password": fields.String(),
        "contact": fields.Integer()
        }    
)

UserNewDump = user_ns.model(
    "SignUp_Response Model",
    {
        "public_id": fields.Integer(),
        "email": fields.String(),
        "username": fields.String(),
        "password": fields.String(),
        "date_created": fields.Date(),
        "contact": fields.Integer()
        }    
)       

UsersDump = user_ns.model(
    "List Of Users",{
       "public_id": fields.Integer(),
        "username": fields.String(),
        }
)


UserLoginLoad = user_ns.model(
    "Login_Request Model",
    {
        "username_email": fields.String(),
        "password": fields.String()
    }
)

UserLoginDump = user_ns.model(
   "Login_Response Model",
    {
        "username": fields.String(),
        "access_token": fields.String() 
    } 
)


UserUpdate = user_ns.model(
    "Update_Request Model",
    {
        "email": fields.String(),
        "username": fields.String(),
        "contact": fields.Integer()
        }
)

UserPasswordUpdate = user_ns.model(
    "Update Password Model",
    {
        "email": fields.String(),
        "password": fields.String(),
        "confirm_password": fields.String()
    }
)

