from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_restplus import Api, Resource

app = Flask(__name__)
api = Api(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# app.config['POSTGRES_URL'] = "postgresql://postgres:postgres@localhost:5432/organization"

from app import routes, models
