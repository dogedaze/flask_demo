from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@localhost:5432/postgres'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap=Bootstrap(app)
from app import routes, models