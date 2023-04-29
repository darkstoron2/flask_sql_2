from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired


class AddDepForm(FlaskForm):
    title = StringField('Название департамента', validators=[DataRequired()])
    members = StringField('Участники')
    email = StringField('Почта')
    submit = SubmitField('Добавить')
