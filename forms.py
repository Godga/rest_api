from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class ArticleForm(FlaskForm):
	author = StringField('author', validators=[DataRequired(), Length(min=3, max=80)])
	content = StringField('content', validators=[DataRequired(), Length(min=3, max=80)])