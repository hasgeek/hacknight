# -*- coding: utf-8 -*-

from flask import render_template, request, redirect
from hacknight import app, baseframe
from hacknight.models.event import Event, EVENT_STATUS, Redirect, Profile
from datetime import datetime
from pytz import utc


@app.route('/')
def index():
    # TODO: Filter events by status
    upcoming_events = Event.query.filter(Event.end_datetime > datetime.utcnow(), Event.status != EVENT_STATUS.DRAFT, Event.status != EVENT_STATUS.CANCELLED).order_by(Event.start_datetime.asc()).all()
    past_events = Event.query.filter(Event.end_datetime < datetime.utcnow(), Event.status != EVENT_STATUS.DRAFT, Event.status != EVENT_STATUS.CANCELLED).order_by(Event.end_datetime.desc()).all()
    return render_template('index.html', upcoming_events=upcoming_events, past_events=past_events)


@app.template_filter('shortdate')
def shortdate(date):
    return utc.localize(date).astimezone(app.config['tz']).strftime("%B %d, %Y")


@app.template_filter('fulldate')
def fulldate(date):
    return utc.localize(date).astimezone(app.config['tz']).strftime("%a, %b %e %l:%M %p")


@app.template_filter('weekdate')
def weekdate(date):
    return utc.localize(date).astimezone(app.config['tz']).strftime("%a, %b %e")


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


@baseframe.app_errorhandler(404)
def page_not_found(e):
    r = request.view_args
    if r and 'profile' in r and 'event' in r:
        profile = Profile.query.filter_by(name=r['profile']).first()
        if profile:
            redirect_to = Redirect.query.filter_by(profile=profile, old_event_name=r['event']).first()
            if redirect_to:
                return redirect(redirect_to.event.url_for(), 302)
    return render_template('404.html'), 404
