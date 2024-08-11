import os
from datetime import datetime

from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from config import Config
from forms import NewBirthdayForm

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

class Birthday(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lastname = db.Column(db.String(100), nullable=False)
    firstname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    birthday = db.Column(db.Date)
    seven_day_notify = db.Column(db.Boolean) 
    one_day_notify = db.Column(db.Boolean)
    same_day_notify = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    
    def __repr__(self):
        return f'<Birthday {self.firstname}>'
    
@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.route('/')
def index():
    app.logger.debug("Getting  birthdays and sorting...")
    birthdays = Birthday.query.order_by(Birthday.birthday.desc()).all()
    return render_template("index.html", birthdays = birthdays)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/birthdays", methods = ('GET','POST'))
def birthday_page():
    form = NewBirthdayForm()
    if form.validate_on_submit():
        app.logger.debug("Reading form...")
        lname = form.lastname.data
        fname = form.firstname.data
        email = form.email.data
        bday = form.birthday.data
        seven_day = form.seven_day_notify.data
        one_day = form.one_day_notify.data
        same_day = form.same_day_notify.data

        new_bday = Birthday(lastname=lname, firstname=fname, email=email, birthday=bday, seven_day_notify=seven_day, one_day_notify=one_day, same_day_notify=same_day)
        app.logger.info("Adding new birthday to db")
        db.session.add(new_bday)
        db.session.commit()

        return redirect(url_for('index'))
    app.logger.debug("Getting  birthdays and sorting...")
    return render_template("birthdays.html", form=form)

@app.route("/users")
def users_page():
    try:
        return render_template('users_fake.html')
    except:
        abort(404)

@app.route('/500')
def error500():
    abort(500)