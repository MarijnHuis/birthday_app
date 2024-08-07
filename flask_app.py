import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

from config import Config

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

# def add_birthday(lname, fname, email, bday, seven_day, one_day, same_day):
#     # currently breaks if email not unique
#     new_bday = Birthday(lastname=lname, firstname=fname, email=email, birthday=datetime.strptime(bday, "%Y-%m-%d"), seven_day_notify=seven_day, one_day_notify=one_day, same_day_notify=same_day)
#     db.session.add(new_bday)
#     db.session.commit()

@app.route('/')
def index():
    birthdays = Birthday.query.order_by(Birthday.birthday.desc()).all()
    return render_template("index.html", birthdays = birthdays)

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/birthdays/", methods = ('GET','POST'))
def birthday_page():
    if request.method == 'POST':
        lname = request.form["lname"]
        fname = request.form["fname"]
        email = request.form["email"]
        bday = request.form["bday"]
        reminders = request.form.getlist("mycheckbox")
        seven_day = 1 if "7" in reminders else 0
        one_day = 1 if "1" in reminders else 0
        same_day = 1 if "0" in reminders else 0

        new_bday = Birthday(lastname=lname, firstname=fname, email=email, birthday=datetime.strptime(bday, "%Y-%m-%d"), seven_day_notify=seven_day, one_day_notify=one_day, same_day_notify=same_day)
        db.session.add(new_bday)
        db.session.commit()

        return redirect(url_for('index'))
    
    birthdays = Birthday.query.order_by(Birthday.birthday.desc()).all()
    return render_template("birthdays.html", birthdays=birthdays)