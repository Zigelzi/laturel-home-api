from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
# Enable Cross Origin Resource Sharing (CORS)
CORS(app, resources={r'/*':{'origins':'*'}}) 

db = SQLAlchemy(app)

from home_api import routes