#!/usr/bin/python3
"""
"""
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, make_response, jsonify

app = Flask(__name__)

@app.teardown_appcontext
def tear_down(self):
    """
    close the session
    """
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """
    return 404 status code response
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    # Register the blueprint with the app
    app.register_blueprint(app_views, url_prefix='/api/v1')
    app.run(host=getenv("HBNB_API_HOST", "0.0.0.0"),
            port=int(getenv("HBNB_API_PORT", "5000")), threaded=True)
