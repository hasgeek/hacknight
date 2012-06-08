# -*- coding: utf-8 -*-

from flask import render_template, abort, flash, url_for
from coaster.views import load_model, load_models
from baseframe.forms import render_redirect, render_form, render_delete_sqla
from hacknight import app
from hacknight.models import db, Profile
from hacknight.models.event import Event, EventStatus
from hacknight.models.participant import Participant
from hacknight.forms.event import EventForm
from hacknight.views.login import lastuser
import pytz


@app.route('/<profile>/<event>', methods=["GET"])
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event'}, 'event'))
def event_view(profile, event):
    participants = Participant.query.filter_by(event_id = event.id) 
    return render_template('event.html', event=event, timezone=event.start_datetime.strftime("%Z"), participants=participants)

@app.route('/<profile>/new', methods=['GET', 'POST'])
@lastuser.requires_login
@load_model(Profile, {'name': 'profile'}, 'profile')
def event_new(profile):
    form = EventForm()
    if form.validate_on_submit():
        event = Event()
        form.populate_obj(event)
        event.make_name()
        event.start_datetime = event.start_datetime.replace(tzinfo=pytz.timezone(event.event_timezone))
        event.end_datetime = event.end_datetime.replace(tzinfo=pytz.timezone(event.event_timezone))
        event.profile_id = profile.id
        db.session.add(event)
        db.session.commit()
        flash(u"You have created new event", "success")
        values={'profile': profile.name, 'event': event.name}
        return render_redirect(url_for('event_view', **values), code=303)
    return render_form(form=form, title="New Event", submit=u"Create",
        cancel_url=url_for('profile_view', profile=profile.name), ajax=False)

@app.route('/<profile>/<event>/edit', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_edit(profile, event):
    workflow = event.workflow()
    if not workflow.can_edit():
        abort(403)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        form.populate_obj(event)
        event.make_name()
        db.session.add(event)
        db.session.commit()
        flash(u"You have edited details for event %s" % event.title, "success")
        return render_redirect(url_for('event_view', event=event.name, profile=profile.name), code=303)
    return render_form(form=form, title="Edit Event", submit=u"Save",
        cancel_url=url_for('event_view', event=event.name, profile=profile.name), ajax=False)

@app.route('/<profile>/<event>/publish', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_publish(profile, event):
    workflow = event.workflow()
    if not workflow.can_edit():
        abort(403)
    event.status = EventStatus.PUBLISHED
    db.session.add(event)
    db.session.commit()
    flash(u"You have published the event %s" % event.title, "success")
    return render_redirect(url_for('event_view', event=event.name, profile=profile.name), code=303)

@app.route('/<profile>/<event>/cancel', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_cancel(profile, event):
    workflow = event.workflow()
    if not workflow.can_delete():
        abort(403)
    event.status = EventStatus.CANCELLED
    db.session.add(event)
    db.session.commit()
    flash(u"You have cancelled event %s" % event.title, "success")
    return render_redirect(url_for('profile_view', profile=profile.name), code=303)

@app.route('/<profile>/<event>/delete', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_delete(profile, event):
    workflow = event.workflow()
    if not workflow.can_delete():
        abort(403)
    return render_delete_sqla(event, db, title=u"Confirm delete",
        message=u"Delete Event '%s'? This cannot be undone." % event.title,
        success=u"You have deleted an event '%s'." % event.title,
         next=url_for('profile_view', profile=profile.name))

