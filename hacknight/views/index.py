# -*- coding: utf-8 -*-

from flask import render_template
from hacknight import app
from hacknight.models.event import Event
from pytz import utc, timezone

tz = timezone(app.config['TIMEZONE'])

@app.route('/')
def index():
	events = Event.query.filter_by(status=0).all()
	return render_template('index.html', events=events)


@app.template_filter('shortdate')
def shortdate(date):
    return utc.localize(date).astimezone(tz).strftime("%B %d, %Y")
