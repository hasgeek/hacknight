# -*- coding: utf-8 -*-

from flask import render_template
from hacknight import app
from hacknight.models.event import Event
from pytz import utc, timezone

tz = timezone(app.config['TIMEZONE'])


@app.route('/')
def index():
    # TODO: Filter events by status
    events = Event.query.order_by(Event.start_datetime.desc()).all()
    return render_template('index.html', events=events)


@app.template_filter('shortdate')
def shortdate(date):
    return utc.localize(date).astimezone(tz).strftime("%B %d, %Y")


@app.template_filter('fulldate')
def fulldate(date):
    return utc.localize(date).astimezone(tz).strftime("%a, %b %e %H:%M %p")


@app.template_filter('weekdate')
def weekdate(date):
    return utc.localize(date).astimezone(tz).strftime("%a, %b %e")


@app.template_filter('cleanurl')
def cleanurl(url):
    if url.startswith('http://'):
        url = url[7:]
    elif url.startswith('https://'):
        url = url[8:]
    if url.endswith('/') and url.count('/') == 1:
        # Remove trailing slash if applied to end of domain name
        # but leave it in if it's a path
        url = url[:-1]
    return url
