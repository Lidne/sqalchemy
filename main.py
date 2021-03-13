import flask
import flask_login
from flask_login import LoginManager
from data import db_session
from forms.user import RegisterForm, LoginForm
from forms.news import NewsForm
from data.users import User
from data.news import News

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/blogs.db")
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
    if flask_login.current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == flask_login.current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return flask.render_template("index.html", news=news)


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


@app.route('/news', methods=['GET', 'POST'])
@flask_login.login_required
def add_news():
    form = NewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = News()
        news.title = form.title.data
        news.content = form.content.data
        news.is_private = form.is_private.data
        flask_login.current_user.news.append(news)
        db_sess.merge(flask_login.current_user)
        db_sess.commit()
        return flask.redirect('/')
    return flask.render_template('news.html', title='Добавление новости',
                                 form=form)


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@flask_login.login_required
def edit_news(id):
    form = NewsForm()
    if flask.request.method == "GET":
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == flask_login.current_user
                                          ).first()
        if news:
            form.title.data = news.title
            form.content.data = news.content
            form.is_private.data = news.is_private
        else:
            flask.abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        news = db_sess.query(News).filter(News.id == id,
                                          News.user == flask_login.current_user
                                          ).first()
        if news:
            news.title = form.title.data
            news.content = form.content.data
            news.is_private = form.is_private.data
            db_sess.commit()
            return flask.redirect('/')
        else:
            flask.abort(404)
    return flask.render_template('news.html',
                                 title='Редактирование новости',
                                 form=form
                                 )


@app.route('/news_delete/<int:id>', methods=['GET', 'POST'])
@flask_login.login_required
def news_delete(id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id,
                                      News.user == flask_login.current_user
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        flask.abort(404)
    return flask.redirect('/')


if __name__ == '__main__':
    main()
