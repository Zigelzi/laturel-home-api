from flask import jsonify

from home_api import app
from home_api.config import Config, DevConfig

@app.route('/home')
def home():
    return jsonify({'taloyhtiö':'hakulinpuisto'})