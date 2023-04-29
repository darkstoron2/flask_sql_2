from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, StringField, IntegerField, DateField
from wtforms.validators import DataRequired


class AddJobForm(FlaskForm):
    job = StringField('Описание работы', validators=[DataRequired()])
    work_size = IntegerField('Продолжительность')
    collaborators = StringField('Участники')
    start_date = DateField('Начало работы')
    end_date = DateField('Начало работы')
    is_finished = BooleanField("Работа завершена")
    submit = SubmitField('Добавить')
