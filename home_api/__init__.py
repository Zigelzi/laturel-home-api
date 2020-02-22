from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow



from home_api.config import Config, DevConfig

app = Flask(__name__)
app.config.from_object(DevConfig)
# Enable Cross Origin Resource Sharing (CORS)
CORS(app, resources={r'/*': {'origins': '*'}})

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Flask-Marshmallow is used for serializing the DB objects to JSON.
ma = Marshmallow(app)

from home_api import routes, models