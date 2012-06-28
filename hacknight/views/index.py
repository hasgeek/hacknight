# -*- coding: utf-8 -*-

from flask import render_template, g
from hacknight import app
from hacknight.models.event import Event
from pytz import utc, timezone
from hacknight.models.event import Profile

tz = timezone(app.config['TIMEZONE'])


@app.route('/')
def index():
    events = Event.query.filter_by(status=0).all()
    if g.user:
        profile = Profile.query.filter_by(userid=g.user.userid).first()
        return render_template('index.html', events=events, profile=profile)
    else:
        return render_template('index.html', events=events)


@app.template_filter('shortdate')
def shortdate(date):
    return utc.localize(date).astimezone(tz).strftime("%B %d, %Y")


@app.template_filter('fulldate')
def fulldate(date):
    return utc.localize(date).astimezone(tz).strftime("%a, %b %e %H: %M %P")
