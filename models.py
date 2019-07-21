from Flask import Flask
from flask_sqlalchemy import SQLAlchemy as sqla
from datetime import datetime
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_object(Config)
db = sqla(app)


class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	author = db.Column(db.String(80), nullable=False)
	content = db.Column(db.Text, nullable=False)
	created = db.Column(db.DateTime, nullable=False, default=datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%SZ"))
	updated = db.Column(db.DateTime, nullable=False, default=datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%SZ"))
	
	def __init__(self, id, author, content, created, updated):
		self.id = id
		self.author = author
		self.content = content
		self.created = created
		self.updated = updated