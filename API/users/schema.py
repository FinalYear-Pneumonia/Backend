from flask_restx import fields
from API.users.controllers import user_ns

UserNewLoad = user_ns.model(
    "SignUp_Request Model",
    {
        "public_id": fields.Integer(),
        "other_name": fields.String(),
        "birth_date": fields.Date(),
        "surname": fields.String(),
        "email": fields.String(),
        "username": fields.String(),
        "password": fields.String(),
        "date_created": fields.Date(),
        "gender": fields.String(),
        "contact": fields.Integer()
        }    
)

UserNewDump = user_ns.model(
    "SignUp_Response Model",
    {
        "public_id": fields.Integer(),
        "other_name": fields.String(),
        "birth_date": fields.Date(),
        "surname": fields.String(),
        "email": fields.String(),
        "username": fields.String(),
        "password": fields.String(),
        "date_created": fields.Date(),
        "gender": fields.String(),
        "contact": fields.Integer()
        }    
)       

UsersDump = user_ns.model(
    "List Of Users",{
       "public_id": fields.Integer(),
        "username": fields.String(),
        "other_name": fields.String(),
        "surname": fields.String(), 
        "gender": fields.String()
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
        "surname": fields.String(),
        "other_name": fields.String(),
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

searchLoad = user_ns.model(
        "Search Model",
        {
            'column_name' : fields.String(),
            "data": fields.String()
        }
    )
