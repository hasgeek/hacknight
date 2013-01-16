#!/usr/bin/env python

from hacknight import app, init_for
from hacknight.models import db
init_for('development')
db.create_all()
app.run('0.0.0.0', debug=True, port=8100)
