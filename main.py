from flask import Flask, render_template, redirect, request, make_response
from data.users import User
from data.jobs import Jobs
from forms.user import RegisterForm
from flask_login import login_user, LoginManager, logout_user, login_required, current_user
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_session.global_init('db/mars_one.db')
db_sess = db_session.create_session()


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
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
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/")
def index():
    jobs = db_sess.query(Jobs)
    return render_template("index.html", jobs=jobs, title='Jobs')


@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
