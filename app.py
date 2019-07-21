from flask import Flask, escape, url_for, request, render_template, make_response, jsonify, redirect
import json
from config import Config
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as sqla
import os
from forms import ArticleForm
from flask_marshmallow import Marshmallow
from werkzeug.exceptions import BadRequest, NotFound


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_object(Config)
#app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///' + os.path.join(basedir, 'rest.db')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = sqla(app)
ma = Marshmallow(app)

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
		
#Schema
class ArticleSchema(ma.Schema):
	class Meta:
		fields = ('id', 'author', 'content', 'created', 'updated')

article_schema = ArticleSchema(strict=True)
articles_schema = ArticleSchema(many=True, strict=True)


#Functions
@app.route('/articles', methods=['GET', 'POST'])
def articles():
	form = ArticleForm()
	if request.method == 'POST':
		# author = request.form['author']
		# content = request.form['content']
		# time = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%SZ")
		# isotime = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
		# art = Article(None, author, content, isotime, isotime)
		# db.session.add(art)
		# db.session.commit()
		# return redirect(url_for('articles'))
		author = request.json['author']
		content = request.json['content']
		time = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%SZ")
		isotime = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
		art = Article(None, author, content, isotime, isotime)
		db.session.add(art)
		db.session.commit()
		return article_schema.jsonify(art)
	elif request.method == 'GET':
		# isotime = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%SZ")
		art_list = None
		if Article.query.all():
			art_list = Article.query.all()
			result = articles_schema.dump(art_list)
		# content={'articles':art_list, 'form':form}
		# resp = make_response(render_template('articles.html', **content))
		# return resp
		return jsonify(result.data)
	

@app.route('/articles/<id>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def article(id):
	if not Article.query.get(id):
		return jsonify({'message':"Couldn't found a article with id={}.".format(id)}), 404
	if request.method == 'GET':
		article = Article.query.get(id)
		return article_schema.jsonify(article)
	if request.method == 'PUT' or request.method == 'PATCH':
		article = Article.query.get(id)
		if article.author != request.json['author']:
			article.author = request.json['author']
		if article.content != request.json['content']:
			article.content = request.json['content']
		time = datetime.strftime(datetime.now(), "%Y-%m-%dT%H:%M:%SZ")
		isotime = datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
		article.updated = isotime
		db.session.commit()
		return article_schema.jsonify(article)
	if request.method == 'DELETE':
		article = Article.query.get(id)
		db.session.delete(article)
		db.session.commit()
		return jsonify({'message':'success'})	


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({'message':'Very bad request'}), 400
	
	
@app.errorhandler(NotFound)
def handle_not_found(e):
    return jsonify({'message':"Page doesn't exist"}), 404


if __name__ == '__main__':
	app.run(debug=True)