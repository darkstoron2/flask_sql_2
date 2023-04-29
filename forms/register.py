from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    surname = StringField("Фамилия пользователя", validators=[DataRequired()])
    name = StringField("Имя пользователя", validators=[DataRequired()])
    age = IntegerField("Возраст")
    position = StringField("Должность пользователя")
    speciality = StringField("Специальность пользователя")
    address = TextAreaField("Адрес")
    submit = SubmitField('Войти')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)