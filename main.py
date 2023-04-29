import login as login
from flask import Flask, render_template, make_response, request, redirect, abort
from data import db_session
from data.departament import Departments
from data.jobs import Jobs
from data.news import News
from data.users import User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.add_dep import AddDepForm
from forms.add_job import AddJobForm
from forms.login import LoginForm
from forms.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/departments')
def departments_table():
    db_sess = db_session.create_session()
    departments = db_sess.query(Departments).all()
    return render_template('departments_table.html', title='Departments', departments=departments)


@app.route('/add_departments',  methods=['GET', 'POST'])
@login_required
def add_departments():
    form = AddDepForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        dep = Departments()
        dep.title = form.title.data
        dep.members = form.members.data
        dep.email = form.email.data
        current_user.dep.append(dep)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/departments')
    return render_template('add_dep.html', title='Добавление департамента',
                           form=form)


@app.route('/departments/<int:deps_id>', methods=['GET', 'POST'])
@login_required
def edit_departments(deps_id):
    db_sess = db_session.create_session()
    deps = db_sess.query(Departments).filter(Departments.id == deps_id).first()
    if current_user.id == 1 or current_user.id == deps.chief:
        form = AddDepForm()
        if request.method == "GET":
            if deps:
                form.title.data = deps.title
                form.members.data = deps.members
                form.email.data = deps.email
            else:
                abort(404)
        if form.validate_on_submit():
            if deps:
                deps.title = form.title.data
                deps.members = form.members.data
                deps.email = form.email.data
                db_sess.commit()
                return redirect('/departments')
            else:
                abort(404)
        return render_template('add_dep.html',
                               title='Редактирование департамента',
                               form=form
                               )
    else:
        abort(404)


@app.route('/departments_delete/<int:deps_id>', methods=['GET', 'POST'])
@login_required
def deps_delete(deps_id):
    db_sess = db_session.create_session()
    deps = db_sess.query(Departments).filter(Departments.id == deps_id).first()
    if deps.chief == current_user.id or current_user.id == 1:
        if deps:
            db_sess.delete(deps)
            db_sess.commit()
        else:
            abort(404)
    else:
        abort(404)
    return redirect('/departments')


@app.route('/')
def jobs_table():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return render_template('jobs_table.html', title='Jobs', jobs=jobs)


@app.route('/add_job',  methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = AddJobForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        job = Jobs()
        job.job = form.job.data
        job.work_size = form.work_size.data
        job.start_date = form.start_date.data
        job.end_date = form.end_date.data
        job.is_finished = form.is_finished.data
        current_user.job.append(job)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Добавление работы',
                           form=form)


# Капитан логин romahubbatulin01358@gmail.com пароль 1234
@app.route('/jobs/<int:jobs_id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == jobs_id).first()
    if current_user.id == 1 or current_user.id == jobs.team_leader:
        form = AddJobForm()
        if request.method == "GET":
            if jobs:
                form.job.data = jobs.job
                form.work_size.data = jobs.work_size
                form.collaborators.data = jobs.collaborators
                form.is_finished.data = True if jobs.is_finished == 1 else False
                form.start_date.data = jobs.start_date
                form.end_date.data = jobs.end_date
            else:
                abort(404)
        if form.validate_on_submit():
            if jobs:
                jobs.job = form.job.data
                jobs.work_size = form.work_size.data
                jobs.collaborators = form.collaborators.data
                jobs.is_finished = form.is_finished.data
                jobs.start_date = form.start_date.data
                jobs.end_date = form.end_date.data
                db_sess.commit()
                return redirect('/')
            else:
                abort(404)
        return render_template('add_job.html',
                               title='Редактирование работы',
                               form=form
                               )
    else:
        abort(404)


@app.route('/jobs_delete/<int:jobs_id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == jobs_id).first()
    if jobs.team_leader == current_user.id or current_user.id == 1:
        if jobs:
            db_sess.delete(jobs)
            db_sess.commit()
        else:
            abort(404)
    else:
        abort(404)
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


def main():
    db_session.global_init("db/mars_explorer.db")
    app.run()


if __name__ == '__main__':
    main()