# -*- coding: utf-8 -*-

from flask import render_template, abort, flash, url_for, g
from coaster.views import load_model, load_models
from baseframe.forms import render_redirect, render_form, render_delete_sqla
from hacknight import app
from hacknight.models import db, Profile
from hacknight.models.event import Event, EventStatus
from hacknight.models.participant import Participant, ParticipantStatus
from hacknight.models.project import Project
from hacknight.forms.event import EventForm, EventManagerForm
from hacknight.views.login import lastuser
import hacknight.views.workflow 
import pytz


@app.route('/<profile>/<event>', methods=["GET"])
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event'}, 'event'))
def event_view(profile, event):
    projects = Project.query.filter_by(event_id=event.id)
    participants = Participant.query.filter_by(event_id = event.id) 
    applied=0
    for p in participants:
        if p.user == g.user and p.status!= ParticipantStatus.WITHDRAWN:
            applied=1
            break
    return render_template('event.html', profile=profile, event=event, projects=projects, timezone=event.start_datetime.strftime("%Z"), participants=participants, applied=applied)

@app.route('/<profile>/new', methods=['GET', 'POST'])
@lastuser.requires_login
@load_model(Profile, {'name': 'profile'}, 'profile')
def event_new(profile):
    form = EventForm()
    if form.validate_on_submit():
        event = Event()
        form.populate_obj(event)
        event.make_name()
        event.start_datetime = event.start_datetime
        event.end_datetime = event.end_datetime
        event.profile_id = profile.id
        db.session.add(event)
        db.session.commit()
        participant = Participant(user_id=g.user.id, event_id=event.id, status=ParticipantStatus.OWNER)
        db.session.add(participant)
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

@app.route('/<profile>/<event>/manage', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_open(profile, event):
    workflow = event.workflow()
    if not workflow.can_open():
        abort(403)
    pending_participants = Participant.query.filter_by(status=ParticipantStatus.PENDING) 
    confirmed_participants = Participant.query.filter_by(status=ParticipantStatus.CONFIRMED) 
    form = EventManagerForm()
    form.make_participants(pending_participants)
    if form.validate_on_submit():
        raise
    return render_form(form=form, title="Manage", submit=u"Create",
        cancel_url=url_for('profile_view', profile=profile.name), ajax=False)
    
#    workflow.open()
#    db.session.add(event)
#    db.session.commit()
#    flash(u"You have edited details for event %s" % event.title, "success")
#    return render_redirect(url_for('event_view', event=event.name, profile=profile.name), code=303)

@app.route('/<profile>/<event>/apply', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_apply(profile, event):
    user_id = g.user.id
    participant = Participant.query.filter_by(event_id=event.id,user_id=user_id).first()
    p = Participant()
    if not participant:
        total_participants = Participant.query.filter_by(event_id=event.id).count()
        participant = Participant()
        participant.user_id=user_id
        participant.event_id=event.id
        participant.status=ParticipantStatus.PENDING if event.maximum_participants < total_participants else ParticipantStatus.WL
        db.session.add(participant)
        db.session.commit()
        flash(u"{0} is added to queue for the event{1}, you will be notified by Event manager".format(g.user.fullname, event.name), "success")
    elif participant.status==ParticipantStatus.WITHDRAWN:
        participant.status=ParticipantStatus.PENDING
        db.session.commit()
    else:
        flash(u"Your request is pending. ", "error")
    values={'profile': profile.name, 'event': event.name}
    return render_redirect(url_for('event_view', **values), code=303)

@app.route('/<profile>/<event>/withdraw', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_withdraw(profile, event):
    user_id = g.user.id
    participant = Participant.query.filter_by(event_id=event.id,user_id=user_id).first()
    if participant:
        workflow = participant.workflow()
        if not workflow.can_withdraw():
            abort(403)
        withdraw_call = {
                         0: workflow.withdraw_pending,
                         1: workflow.withdraw_waiting_list,
                         2: workflow.withdraw_confirmed,
                         3: workflow.withdraw_rejected,
                         }
        try:
            withdraw_call[participant.status]()
        except KeyError:
            pass
        db.session.add(participant)
        db.session.commit()
        flash(u"{0} is withdrawn from the event{1}".format(g.user.fullname, event.name), "success")
        values={'profile': profile.name, 'event': event.name}
        return render_redirect(url_for('event_view', **values), code=303)
    else:
        abort(403)

@app.route('/<profile>/<event>/publish', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_publish(profile, event):
    workflow = event.workflow()
    if not workflow.can_edit():
        abort(403)
    workflow.openit()
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
    if not workflow.can_edit():
        abort(403)
    call = {
            0: workflow.cancel_draft,
            2: workflow.cancel_active
            }
    try:
        call[event.status]()
    except KeyError:
        pass

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

