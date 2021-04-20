import datetime
import random

import flask
import flask_login
from flask_login import LoginManager
from flask_restful import reqparse, abort, Api, Resource
from data import db_session, jobs_api, users_resource
from forms.user import RegisterForm, LoginForm
from forms.jobs import JobsForm
from data.users import User
from data.jobs import Jobs

app = flask.Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/mars_one.db")
    app.register_blueprint(jobs_api.blueprint)
    # для списка объектов
    api.add_resource(users_resource.UsersListResource, '/api/users')

    # для одного объекта
    api.add_resource(users_resource.UsersResource, '/api/users/<int:user_id>')
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            flask_login.login_user(user, remember=form.remember_me.data)
            return flask.redirect("/")
        return flask.render_template('login.html',
                                     message="Неправильный логин или пароль",
                                     form=form)
    return flask.render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return flask.redirect("/")


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    user = db_sess.query(User).first()
    print(user.to_dict())
    return flask.render_template("index.html", jobs=jobs)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return flask.render_template('register.html', title='Регистрация',
                                         form=form,
                                         message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return flask.render_template('register.html', title='Регистрация',
                                         form=form,
                                         message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return flask.redirect('/login')
    return flask.render_template('register.html', title='Регистрация', form=form)


@app.route('/jobs', methods=['GET', 'POST'])
@flask_login.login_required
def add_news():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.job = form.job.data
        jobs.team_leader = form.team_leader.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.start_date = form.start_date.data
        jobs.end_date = form.end_date.data
        jobs.is_finished = form.is_finished.data
        flask_login.current_user.news.append(jobs)
        db_sess.merge(flask_login.current_user)
        db_sess.commit()
        return flask.redirect('/')
    return flask.render_template('jobs.html', title='Добавление работы',
                                 form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@flask_login.login_required
def edit_news(id):
    form = JobsForm()
    if flask.request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == flask_login.current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            flask.abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == flask_login.current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return flask.redirect('/')
        else:
            flask.abort(404)
    return flask.render_template('jobs.html',
                                 title='Редактирование новости',
                                 form=form
                                 )


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@flask_login.login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).filter(Jobs.id == id,
                                      Jobs.user == flask_login.current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        flask.abort(404)
    return flask.redirect('/')


if __name__ == '__main__':
    main()
