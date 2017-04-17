# -*- coding: utf-8 -*-

from flask import render_template, request, redirect
from hacknight import app, baseframe
from hacknight.models.event import Event, EventRedirect, Profile
from pytz import utc, timezone as pytz_timezone


@app.route('/')
def index():
    # TODO: Filter events by status
    upcoming_events = Event.upcoming_events()
    past_events = Event.past_events()
    return render_template('index.html', upcoming_events=upcoming_events, past_events=past_events)


@app.template_filter('startdate')
def startdate(date, timezone=None):
    if timezone:
        tz = pytz_timezone(timezone)
    else:
        tz = app.config['tz']
    return tz.normalize(utc.localize(date).astimezone(tz)).strftime("%a, %e %b %l:%M %p")


@app.template_filter('enddate')
def enddate(date, timezone=None):
    if timezone:
        tz = pytz_timezone(timezone)
    else:
        tz = app.config['tz']
    return tz.normalize(utc.localize(date).astimezone(tz)).strftime("%l:%M %p %e %b %Y")


@app.template_filter('shortdate')
def shortdate(date, timezone=None):
    if timezone:
        tz = pytz_timezone(timezone)
    else:
        tz = app.config['tz']
    return tz.normalize(utc.localize(date).astimezone(tz)).strftime("%e %B %Y")


@app.template_filter('fulldate')
def fulldate(date, timezone=None):
    if timezone:
        tz = pytz_timezone(timezone)
    else:
        tz = app.config['tz']
    return tz.normalize(utc.localize(date).astimezone(tz)).strftime("%a, %e %b %l:%M %p")


@app.template_filter('weekdate')
def weekdate(date, timezone=None):
    if timezone:
        tz = pytz_timezone(timezone)
    else:
        tz = app.config['tz']
    return tz.normalize(utc.localize(date).astimezone(tz)).strftime("%a, %e %b")


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
            redirect_to = EventRedirect.query.filter_by(profile=profile, name=r['event']).first()
            if redirect_to:
                return redirect(redirect_to.event.url_for(), 302)
    return render_template('404.html'), 404
