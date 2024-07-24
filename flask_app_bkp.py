# A very simple Flask Hello World app for you to get started with...
import os
import sqlite3

import mysql.connector
from flask import Flask, render_template, request

from config import Config

app = Flask(__name__)

if Config.SQL_DATABASE_URI == "mysql":
    try:
        mydb = mysql.connector.connect(
        host="pim1.mysql.pythonanywhere-services.com",
        user="pim1",
        password="mysqladmin",
        database="pim1$birthdays"
        )
        message = f"DB {Config.SQL_DATABASE_URI} is connected!"
        mycursor = mydb.cursor()

    except mysql.connector.Error:
        data = []
        message = f"DB {Config.SQL_DATABASE_URI} is NOT connected!"
else:
    try:
        # basedir = os.path.dirname(__file__)
        db_name = "birthdays.db"
        mydb = sqlite3.connect(db_name, check_same_thread=False)
        message = f"DB {Config.SQL_DATABASE_URI} is connected!"
        mycursor = mydb.cursor()
        # mycursor.execute("""
        #     CREATE TABLE Birthdays (
        #         ID INTEGER NOT NULL,
        #         LastName varchar(255) NOT NULL,
        #         FirstName varchar(255) NOT NULL,
        #         Email varchar(255),
        #         Birthday date NOT NULL,
        #         SevenDayReminder boolean NOT NULL DEFAULT 1,
        #         OneDayReminder boolean NOT NULL DEFAULT 1,
        #         SameDayReminder boolean NOT NULL DEFAULT 1,
        #         PRIMARY KEY (ID)
        #     );
        #     """)
        # mydb.commit()
    except sqlite3.Error as e:
        data = []
        message = f"DB {Config.SQL_DATABASE_URI} is NOT connected! Error: {e}"

# Birthday(lastname="Huis", firstname="Marijn", email="marijn2huis@gmail.com", birthday=datetime(1997,8,16), seven_day_notify=0, one_day_notify=1, same_day_notify=1)
def add_birthday(lname, fname, email, bday, seven_day, one_day, same_day):
    query = "INSERT INTO Birthdays (LastName,FirstName,Email,Birthday,SevenDayReminder,OneDayReminder,SameDayReminder) VALUES (?,?,?,?,?,?,?);"
    values = (lname, fname, email, bday, seven_day, one_day, same_day)
    mycursor.execute(query, values)
    mydb.commit()

@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        lname = request.form["lname"]
        fname = request.form["fname"]
        email = request.form["email"]
        bday = request.form["bday"]
        reminders = request.form.getlist("mycheckbox")
        seven_day = 1 if "7" in reminders else 0
        one_day = 1 if "1" in reminders else 0
        same_day = 1 if "0" in reminders else 0
        add_birthday(lname, fname, email, bday, seven_day, one_day, same_day)
    # mycursor.execute("SELECT * FROM Birthdays ORDER BY Birthday DESC;")
    try:
        mycursor.execute("SELECT * FROM Birthdays;")
        data = mycursor.fetchall()
    except sqlite3.OperationalError:
        data = []
    return render_template("index.html", message=message, data=data)

