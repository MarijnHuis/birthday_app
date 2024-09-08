from urllib.parse import urlsplit

import sqlalchemy as sa
from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import app, db
from app.forms import LoginForm, NewBirthdayForm
from app.models import Birthday, User


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.route('/')
@login_required
def index():
    app.logger.debug("Getting  birthdays and sorting...")
    query = sa.select(Birthday).order_by(Birthday.birthday.desc())
    birthdays = db.session.scalars(query).all()
    return render_template("index.html", birthdays = birthdays)

@app.route("/about")
@login_required
def about():
    return render_template("about.html")

@app.route("/birthdays", methods = ('GET','POST'))
@login_required
def birthday_page():
    form = NewBirthdayForm()
    if form.validate_on_submit():
        app.logger.debug("Reading form...")
        lname = form.lastname.data
        fname = form.firstname.data
        email = form.email.data
        bday = form.birthday.data

        new_bday = Birthday(lastname=lname, firstname=fname, email=email, birthday=bday)
        app.logger.info("Adding new birthday to db")

        return redirect(url_for('index'))
    app.logger.debug("Getting  birthdays and sorting...")

    query = sa.select(Birthday).order_by(Birthday.firstname.asc())
    birthdays = db.session.scalars(query).all()

    return render_template("birthdays.html", form=form, birthdays=birthdays)

@app.route("/user/<username>")
@login_required
def user_page(username):
    user: User = db.first_or_404(sa.select(User).where(User.username==username))
    birthdays: Birthday = user.following
    return render_template('user.html', user=user, birthdays=birthdays)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/500')
def error500():
    abort(500)