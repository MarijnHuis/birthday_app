from datetime import datetime
from typing import Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


class Birthday(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    lastname: so.Mapped[str]= so.mapped_column(sa.String(100), nullable=False)
    firstname: so.Mapped[str]= so.mapped_column(sa.String(100), nullable=False)
    email: so.Mapped[str]= so.mapped_column(sa.String(80), unique=True, nullable=False)
    birthday: so.Mapped[datetime] = so.mapped_column(sa.Date)
    seven_day_notify: so.Mapped[bool] = so.mapped_column(sa.Boolean) 
    one_day_notify: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    same_day_notify: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f'<Birthday {self.firstname} {self.lastname}>'
    
class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
    