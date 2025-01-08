from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_session import Session

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
session = Session()
