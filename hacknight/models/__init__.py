# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
from hacknight import app
from coaster.sqlalchemy import BaseMixin, BaseNameMixin, BaseScopedNameMixin, BaseScopedIdNameMixin, BaseScopedIdMixin

db = SQLAlchemy(app)

from hacknight.models.user import *
from hacknight.models.event import *
from hacknight.models.venue import *
from hacknight.models.project import *
from hacknight.models.participant import *
from hacknight.models.sponsor import *
