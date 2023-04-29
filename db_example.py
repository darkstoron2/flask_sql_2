from data import db_session
from data.users import User

db_session.global_init("db/blogs.db")

user = User()
user.name = "Пользователь 1"
user.about = "биография пользователя 1"
user.email = "email@email.ru"
db_sess = db_session.create_session()
db_sess.add(user)
db_sess.commit()
