# birthday_app
Webapp for friends to track birthdays

## Create environment
`pip install -r requirements.txt`

## First time to run:
Activate flask app in Python shell

`flask shell`

Import db instance from flask_app 

`from flask_app import db`

Create database and tables (does nothing if already exists)

`db.create_all()`

Drop all tables

`db.drop_all()`

To update tables first drop then re-add