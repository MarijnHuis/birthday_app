from datetime import datetime
from typing import List, Optional

import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from sqlalchemy import func
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login

user_birthday = sa.Table(
    'user_birthday', db.metadata,
    sa.Column("user_id", sa.Integer, sa.ForeignKey('user.id'), primary_key=True),
    sa.Column("birthday_id", sa.Integer, sa.ForeignKey('birthday.id'), primary_key=True)
)

class Birthday(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    lastname: so.Mapped[str]= so.mapped_column(sa.String(100), nullable=False)
    firstname: so.Mapped[str]= so.mapped_column(sa.String(100), nullable=False)
    birthday: so.Mapped[datetime] = so.mapped_column(sa.Date, nullable=False)
    email: so.Mapped[str]= so.mapped_column(sa.String(80), unique=True, nullable=False)

    # this is just a python list can use as normal
    followers: so.Mapped[List['User']] = so.relationship(
        secondary=user_birthday, back_populates='following'
        )
    
    def followers_count(self):
        return len(self.followers)

    def __repr__(self):
        return f'<Birthday {self.firstname} {self.lastname}>'
    
class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    
    seven_day_notify: so.Mapped[bool] = so.mapped_column(sa.Boolean) 
    one_day_notify: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    same_day_notify: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime(timezone=True), server_default=func.now())

    # this is just a python list can use as normal
    following: so.Mapped[List['Birthday']] = so.relationship(
        secondary=user_birthday, back_populates='followers'
        )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_following(self, birthday):
        return birthday in self.following
    
    def follow(self, birthday):
        if not self.is_following(birthday):
            self.following.append(birthday)

    def unfollow(self, birthday):
        if self.is_following(birthday):
            self.following.remove(birthday)

    def following_count(self):
        return len(self.following)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
    