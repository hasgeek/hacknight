#!/usr/bin/env python
import os
os.environ['ENVIRONMENT'] = "development"
from hacknight import app
from hacknight.models import db
db.create_all()
app.run('0.0.0.0', debug=True, port=8100)
