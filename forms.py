from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, EmailField, StringField
from wtforms.validators import DataRequired, Email, Length


class NewBirthdayForm(FlaskForm):
    lastname = StringField("Last Name", validators=[DataRequired(), Length(max=100)])
    firstname = StringField("First Name", validators=[DataRequired(), Length(max=100)])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    birthday = DateField("Birthday", validators=[DataRequired()])
    seven_day_notify = BooleanField("Seven Day Notification")
    one_day_notify = BooleanField("One Day Notification")
    same_day_notify = BooleanField("Same Day Notification")