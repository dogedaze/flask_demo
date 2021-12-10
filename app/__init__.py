from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_bootstrap import Bootstrap
import pymongo
import json
import requests
from modules import db

app = Flask(__name__)
app.config.from_object(Config)
client = pymongo.MongoClient("mongodb://pythonforfinance:mypassword@cluster0-shard-00-00-apl4w.mongodb.net:27017,cluster0-shard-00-01-apl4w.mongodb.net:27017,cluster0-shard-00-02-apl4w.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client['historical_prices']
migrate = Migrate(app, db)
bootstrap=Bootstrap(app)
from app import routes, models