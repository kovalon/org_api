from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)

from app import routes

# app.config['POSTGRES_URL'] = "postgresql://postgres:postgres@localhost:5432/organization"
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from app import routes, models
