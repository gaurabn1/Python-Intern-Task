from os import access
from flask import jsonify, Blueprint, request, session, redirect
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from models import User, Revoked_Token
from app import db
from extensions import bcrypt


auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route("/register", methods=['POST'])
def register():
    '''
    This endpoint allows new users to register
    - Method: POST
    '''
    data = request.get_json()

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

    if not email and not password:
        return jsonify({"message": "Email and Password are required!"}), 400    

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User already exist!"}), 409

    # Hash password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User Registered!!"}), 201

@auth_blueprint.route("/login", methods=['POST'])
def login():
    '''
    This endpoint allows existing users to login
    - Method: POST
    '''
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    # check if user exists and check password
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"message": "User Logged In!!", "access_token": access_token}), 200
    else:
        return jsonify({"message": "Invalid user credentials!!"}), 401

@auth_blueprint.route("/logout", methods=['POST'])
@jwt_required()
def logout():
    '''
    This endpoint allows authenticated users to logout
    - Method: POST
    '''
    jti = get_jwt()["jti"]
    revoked_token = Revoked_Token(jti=jti)
    db.session.add(revoked_token)
    db.session.commit()
    return jsonify({"message": "User Logged Out!!"}), 200
