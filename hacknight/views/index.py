# -*- coding: utf-8 -*-

from flask import render_template, request, redirect
from hacknight import app, baseframe
from hacknight.models.event import Event, EventRedirect, Profile
from pytz import utc


@app.route('/')
def index():
    # TODO: Filter events by status
    upcoming_events = Event.upcoming_events()
    past_events = Event.past_events()
    return render_template('index.html', upcoming_events=upcoming_events, past_events=past_events)


@app.template_filter('startdate')
def startdate(date):
    return app.config['tz'].normalize(utc.localize(date).astimezone(app.config['tz'])).strftime("%a, %e %b %l:%M %p")


@app.template_filter('enddate')
def enddate(date):
    return app.config['tz'].normalize(utc.localize(date).astimezone(app.config['tz'])).strftime("%l:%M %p %e %b %Y")


@app.template_filter('shortdate')
def shortdate(date):
    return app.config['tz'].normalize(utc.localize(date).astimezone(app.config['tz'])).strftime("%B %d, %Y")


@app.template_filter('fulldate')
def fulldate(date):
    return app.config['tz'].normalize(utc.localize(date).astimezone(app.config['tz'])).strftime("%a, %b %e %l:%M %p")


@app.template_filter('weekdate')
def weekdate(date):
    return app.config['tz'].normalize(utc.localize(date).astimezone(app.config['tz'])).strftime("%a, %b %e")


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
