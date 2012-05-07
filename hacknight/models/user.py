# -*- coding: utf-8 -*-

from flask import g
from flask.ext.lastuser.sqlalchemy import UserBase
from hacknight.models import db

__all__ = ['User']

class User(db.Model, UserBase):
    __tablename__ = 'user'
