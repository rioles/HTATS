from flask import Flask, make_response, jsonify, redirect, request
from flask_cors import CORS, cross_origin
from models import storage
from api.v1.endpoints import app_views
import os
import secrets

from os import getenv

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
#app.config['SECRET_KEY'] = secrets.token_hex(16)

cors = CORS(app, resources={r"api/v1/*": {"origins": "*"}})
app.register_blueprint(app_views)

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
