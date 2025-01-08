from extensions import jwt
from flask import jsonify
from models import Revoked_Token

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_headers, jwt_payload):
    jti = jwt_payload.get("jti")
    print("jwt: ", jwt)
    token = Revoked_Token.query.filter_by(jti=jti).first()
    return token is not None

@jwt.revoked_token_loader
def revoked_token_callback(jwt_headers, jwt_payload):
    return jsonify({"message": "The token has been revoked, Please login again"}), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_headers, jwt_payload):
    return jsonify({"msg": "Token has expired, Please login again."}), 401

