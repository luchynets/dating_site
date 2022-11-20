from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import config


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER

db = SQLAlchemy()
db.init_app(app)

with app.app_context():
	db.create_all() 