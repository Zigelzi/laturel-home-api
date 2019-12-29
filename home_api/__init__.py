from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from home_api.config import Config, DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
# Enable Cross Origin Resource Sharing (CORS)
CORS(app, resources={r'/*': {'origins': '*'}})

db = SQLAlchemy(app)

from home_api import routes