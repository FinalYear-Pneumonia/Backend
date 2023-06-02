
from os import link
from re import search
from tarfile import LENGTH_LINK
from flask import request, make_response, jsonify
from flask_restx import Resource, Namespace
from API.constants.http_status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_406_NOT_ACCEPTABLE, HTTP_409_CONFLICT
from API.extensions import database, mail
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from flask_restx import Api
from flask_jwt_extended import create_access_token,create_refresh_token
import API.users.models as userModel
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from flask_mail import Message
from  sqlalchemy import select
User = userModel.User
user_ns = Namespace("user", description="User Authentications")
from API.users.schema import UserNewLoad, UserNewDump, UserLoginLoad, UserLoginDump, UserUpdate,UsersDump, UserPasswordUpdate

api = Api()




@user_ns.route('/hello')
class HelloResource(Resource):
    def get(self):
        return{'message': 'hello world'}
    
@user_ns.route("/signup")
class SignUP(Resource):
    
    @user_ns.marshal_with(UserNewDump)
    @user_ns.expect(UserNewLoad)
    def post(self):
        """Sign up by fillig the required spaces"""
        
        #get user response
        data = request.get_json()
        email = data.get('email')
        confirm_password = data.get('confirm-password')
        password = data.get("password")
        contact = data.get("contact")
        username = data.get("username")
        
        #check if already in database
        db_user = User.query.filter_by(email=email).first() 
        if db_user:
            abort(HTTP_409_CONFLICT, {"message": f"User with email {email} already exist"})
           
        if password == confirm_password:
            new_user = User(
            email=email,
            password=generate_password_hash(password),
            contact=contact,
            username=username
        )
            userModel.User.save(new_user)
            db_user = User.query.filter_by(email=email).first()            
            new_user_mail(db_user, db_user.public_id)
                
            return  new_user, HTTP_200_OK#jsonify({"message": "done!"})
        else:
            return jsonify({"message": "Password do not match"})
            
    
@user_ns.route("/login")
class LogIn(Resource):
    
    @user_ns.marshal_with(UserLoginDump)
    @user_ns.expect(UserLoginLoad)
    def post(self):
        """LogIn by username & password"""
        
        #get user respsonse
        data = request.get_json()
        username_email = data.get('username_email')
        password = data.get('password')
        
        _new = search(".com$", username_email)

        if _new:
            db_user = User.query.filter_by(email=username_email).first()
        else:
            db_user = User.query.filter_by(username=username_email).first()

        #check if in database
        if db_user:
            passcode=db_user.password
            if check_password_hash(passcode, password):
                db_user.access_token = create_access_token(identity=db_user.public_id)
                return db_user
            abort(HTTP_400_BAD_REQUEST, {"message": "Incorrect Username or password"})
        abort(HTTP_400_BAD_REQUEST, {"message": f"Wrong credentials"})
        #return db_user
        
        
    
    
    
    
    
    
@user_ns.route('/users')
class UsersResource(Resource):

    @user_ns.marshal_list_with(UsersDump)
    # @jwt_required()    
    def get(self):
        """Get all users"""

        users = User.query.all()
        return users, HTTP_200_OK


@user_ns.route('/user/password_reset')
class PasswordResetResource(Resource):
    @user_ns.marshal_with(UserPasswordUpdate)
    def post(self, email):
        data = request.get_json()
        email = data.get('username_email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        user = User.query.filter_by(email=email).first()
        if password == confirm_password:
            user.password = generate_password_hash(password)
            return jsonify("Success"), HTTP_200_OK
        else:
            return jsonify("Passwords do not match"), HTTP_409_CONFLICT
        
            



@user_ns.route('/user/<int:public_id>')
class UserResource(Resource):
    
    @user_ns.marshal_with(UserNewDump)
    # @jwt_required()
    def get(self, public_id):
        """Get user by public_id"""
        user = User.query.get_or_404(public_id)
        if user:
            return user
        abort(404, "User not found")

    @user_ns.expect(UserUpdate)
    @jwt_required()
    @user_ns.marshal_with(UserNewDump)
    def put(self, public_id):
        """Update a user by public_id"""
        user_to_update = User.query.get_or_404(public_id)
        data = request.get_json()
        
        user_to_update.update_user(
                        username=data.get('username'),
                        email=data.get('email'),
                        contact=data.get('contact'),
                        )
        msg = Message('Account Update', recipients=[data.get('email')])
        link = str(api.url_for(LogIn, _external=True))
        msg.body = f"<p><h2>Account Updated Successfully</h2><br>Click on link to go to the Login page. <a href={link}>Click Here</a></p>"
        mail.send(msg)
        update = User.query.get_or_404(public_id)
        return update

    #@user_ns.marshal_with(UserNewDump)
    @jwt_required()
    def delete(self, public_id):
        """Delete a user by public_id"""
        user_to_be_deleted = User.query.get_or_404(public_id)
        if user_to_be_deleted:
            User.delete_user(user_to_be_deleted)
            deleted_user_mail(user_to_be_deleted)
            return jsonify({"message":"User has been deleted successfully"})
        abort(HTTP_404_NOT_FOUND, "No such User found")
    
        
        



            
        
        
        
def new_user_mail(user, user_id):
    email = str(user.email)
    username = user.username
    password = user.password           
    msg = Message('SignUp Account', recipients=[email])
    link = f"https://frontend-team-legacy-health-service.vercel.app/Login"
    msg.body = f"<p><h2>Account Created Successfully</h2><br>You have successfully registered as a .<br>Your Special Identification Number, Username and Password are given below.<br><b>Identification Number:&nbsp;&nbsp; {user_id}</b><br><b>Username:&nbsp;&nbsp;{username}</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>Password:&nbsp;&nbsp;{password}</b><br><b>Please ensure that you note it down as you will use for login.</b><br>Click on link to go to the Login page. <a href={link}>Click Here</a></p>"
    mail.send(msg)
    
def  deleted_user_mail(user):
    email = str(user.email)
    msg = Message('Account Deleted', recipients=[email])
    # link = str(api.url_for(NotificationResource, _external=True))
    msg.body = f"<p><h2>Your account has been <b>DELETED<b>!.</h2><br> If you have no idea why you are receiving this email, please notify the administrator.<a href={link}>Click Here</a></p>"
    mail.send(msg)



