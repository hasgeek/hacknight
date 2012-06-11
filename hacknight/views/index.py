# -*- coding: utf-8 -*-

from flask import render_template
from hacknight import app
from hacknight.models.event import Event


@app.route('/')
def index():
	events = Event.query.filter_by(status=0).all()
	return render_template('index.html', events=events)
