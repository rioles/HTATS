from flask import Flask, make_response, jsonify, redirect, request
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager
from models import storage
from models.token_block_list import TokenBlockList
from models.user import User
from api.v1.endpoints import app_views
import os
import secrets

from os import getenv

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['FLASK_JWT_SECRET_KEY'] = secrets.token_hex(12)
#FLASK_JWT_SECRET_KEY= secrets.token_hex(12)
jwt = JWTManager(app)
cors = CORS(app, resources={r"api/v1/*": {"origins": "*"}})
app.register_blueprint(app_views)


@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    # identity is the result of identity() function
    # You can add any additional claims based on the identity
    # For example, you might fetch additional user information from a database
    user_info = {'role': 'admin'}  # Additional claim: 'role'
    return user_info

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]  # Assuming the 'sub' claim in the JWT represents the user identity
    # Lookup the user based on the identity
    user = storage.find_by(User, **{"email": identity})
    return user

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"msg": "Token has expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    return jsonify({"msg": "Invalid token", "status": 401}), 401

@jwt.unauthorized_loader
def unauthorized_callback(callback_error):
    return jsonify({"msg": "Unauthorized access", "status": 401}), 401

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_data):
    jti = jwt_data["jti"]
    jwti = storage.find_by(TokenBlockList, **{"jti": jti})
    return jwti is not None

@app.teardown_appcontext
def teardown(self):
    """ Calls storage close"""
    storage.close()


@app.errorhandler(404)
def pageNotFound(error):
    """Error handling for 404"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 3001
    #host = getenv('AUT_API_HOST', default='0.0.0.0')
    #port = getenv('AUT_API_PORT', default=3000)
    app.run(host=host, port=port, threaded=True)
