#!/usr/bin/python3
"""
main flask app
"""
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def tear_down(self):
    """
    close the session
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    handles the  404 status code response
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    """
    main entry
    """
    app.register_blueprint(app_views, url_prefix='/api/v1')
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
