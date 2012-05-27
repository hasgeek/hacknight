# -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from hacknight import app
from coaster.sqlalchemy import IdMixin, TimestampMixin, BaseMixin, BaseNameMixin

db = SQLAlchemy(app)

from hacknight.models.user import *
from hacknight.models.organization import *
