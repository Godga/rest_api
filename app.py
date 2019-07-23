from flask import Flask, escape, url_for, request, render_template, make_response, jsonify, redirect
import json
from config import Config
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as sqla
import os
from werkzeug.exceptions import BadRequest, NotFound
from sqlalchemy.ext.declarative import DeclarativeMeta

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_object(Config)
db = sqla(app)

#db
class Article(db.Model):
	__tablename__='article'
	id = db.Column(db.Integer, primary_key=True)
	author = db.Column(db.String(80), nullable=False)
	content = db.Column(db.String(80), nullable=False)
	created = db.Column(db.DateTime, nullable=False, default=datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%SZ"))
	updated = db.Column(db.DateTime, nullable=False, default=datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%SZ"))
	
	def __init__(self, id, author, content, created, updated):
		self.id = id
		self.author = author
		self.content = content
		self.created = created
		self.updated = updated		

	@property
	def serialize(self):
		return {'id':self.id, 'author':self.author, 'content':self.content, 'created':dump_datetime(self.created), 'updated':dump_datetime(self.updated)}

#Functions

def dump_datetime(value):
	if value is None:
		return None
	return value.strftime("%Y-%m-%dT%H:%M:%S")


@app.route('/articles', methods=['GET', 'POST'])
def articles():
	if request.method == 'POST':
		author = request.json['author']
		content = request.json['content']
		time = datetime.now()
		article = Article(None, author, content, time, time)
		db.session.add(article)
		db.session.commit()
		return jsonify([article.serialize])
	elif request.method == 'GET':
		art_list = None
		if Article.query.all():
			art_list = Article.query.all()
		return jsonify([a.serialize for a in art_list])
	

@app.route('/articles/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def article(id):
	article = Article.query.get(id)
	if not article:
		return jsonify({'message':"Couldn't found a article with id={}.".format(id)}), 404
	if request.method == 'GET':
		return jsonify([article.serialize])
	if request.method == 'PUT' or request.method == 'PATCH':
		if article.author != request.json['author']:
			article.author = request.json['author']
		if article.content != request.json['content']:
			article.content = request.json['content']
		#time = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%SZ")
		#isotime = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
		article.updated = datetime.now()
		db.session.commit()
		return jsonify([article.serialize])
	if request.method == 'DELETE':
		db.session.delete(article)
		db.session.commit()
		return jsonify([article.serialize])


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({'message':'Very bad request'}), 400
	
	
@app.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify({'message':"Page doesn't exist"}), 404


if __name__ == '__main__':
	app.run(debug=True)