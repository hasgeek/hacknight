# -*- coding: utf-8 -*-

from sqlalchemy.orm import joinedload
from sqlalchemy import func
import flask.ext.wtf as wtf
from flask import render_template, abort, flash, url_for, g, request, Response, Markup
from coaster.views import load_model, load_models
from baseframe.forms import render_redirect, render_form, render_delete_sqla
from hacknight import app
from hacknight.models import db, Profile, Event, User, Participant, PARTICIPANT_STATUS
from hacknight.forms.event import EventForm, ConfirmWithdrawForm
from hacknight.forms.participant import ParticipantForm
from hacknight.views.login import lastuser


@app.route('/<profile>/<event>', methods=["GET"])
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_view(profile, event):
    participants = [r[0] for r in db.session.query(Participant, User).filter(
        Participant.status != PARTICIPANT_STATUS.WITHDRAWN, Participant.event == event).join(
        (User, Participant.user)).options(
        joinedload(Participant.project_memberships)).order_by(func.lower(User.fullname)).all()]

    accepted_participants = [p for p in participants if p.status == PARTICIPANT_STATUS.CONFIRMED]
    rest_participants = [p for p in participants if p.status != PARTICIPANT_STATUS.CONFIRMED]

    applied = False
    for p in participants:
        if p.user == g.user:
            applied = True
            break
    current_participant = Participant.get(user=g.user, event=event) if g.user else None
    return render_template('event.html', profile=profile, event=event,
        projects=event.projects,
        accepted_participants=accepted_participants,
        rest_participants=rest_participants,
        applied=applied,
        current_participant=current_participant,
        sponsors=event.sponsors)


@app.route('/<profile>/new', methods=['GET', 'POST'])
@lastuser.requires_login
@load_model(Profile, {'name': 'profile'}, 'profile')
def event_new(profile):
    if profile.userid not in g.user.user_organizations_owned_ids():
        abort(403)
    form = EventForm(parent=profile, model=Event)
    form.start_datetime.timezone = app.config['tz']
    form.end_datetime.timezone = app.config['tz']
    if form.validate_on_submit():
        event = Event(profile=profile)
        form.populate_obj(event)
        if not event.name:
            event.make_name()
        db.session.add(event)
        participant = Participant(user=g.user, event=event, status=PARTICIPANT_STATUS.CONFIRMED)
        db.session.add(participant)
        db.session.commit()
        flash(u"New event created", "success")
        return render_redirect(url_for('event_view', profile=profile.name, event=event.name), code=303)
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
        if not event.name:
            event.make_name()
        event.profile_id = profile.id
        db.session.commit()
        flash(u"Your edits to %s are saved" % event.title, "success")
        return render_redirect(url_for('event_view', event=event.name, profile=profile.name), code=303)
    return render_form(form=form, title="Edit Event", submit=u"Save",
        cancel_url=url_for('event_view', event=event.name, profile=profile.name), ajax=False)


participant_status_labels = {
    PARTICIPANT_STATUS.PENDING: "Pending",
    PARTICIPANT_STATUS.WL: "Waiting List",
    PARTICIPANT_STATUS.CONFIRMED: "Confirmed",
    PARTICIPANT_STATUS.REJECTED: "Rejected",
    PARTICIPANT_STATUS.WITHDRAWN: "Withdrawn"
}


@app.template_filter('show_participant_status')
def show_participant_status(status):
    return participant_status_labels[status]


@app.route('/<profile>/<event>/manage', methods=['GET'])
@lastuser.requires_login
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_open(profile, event):
    if  profile.userid not in g.user.user_organizations_owned_ids():
        abort(403)
    participants = Participant.query.filter(
        Participant.status != PARTICIPANT_STATUS.WITHDRAWN,
        Participant.event == event).order_by('created_at')
    return render_template('manage_event.html', profile=profile, event=event,
        participants=participants, statuslabels=participant_status_labels, enumerate=enumerate)


@app.route('/<profile>/<event>/manage/update', methods=['POST'])
@lastuser.requires_login
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_update_participant_status(profile, event):
    if  profile.userid not in g.user.user_organizations_owned_ids():
        return Response("Forbidden", 403)
    participantid = int(request.form['participantid'])
    status = int(request.form['status'])
    participant = Participant.query.get(participantid)

    if(participant.event != event):
        return Response("Forbidden", 403)
    if(participant.status == PARTICIPANT_STATUS.WITHDRAWN):
        return Response("Forbidden", 403)

    participant.status = status
    db.session.commit()
    return "Done"


@app.route('/<profile>/<event>/apply', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_apply(profile, event):
    values = {'profile': profile.name, 'event': event.name}
    participant = Participant.get(g.user, event)
    if not participant:
        # If no participant is found create a new participant entry
        # First collect some information about the new participant
        user = g.user
        form = ParticipantForm(obj=user)
        if form.validate_on_submit():
            total_participants = Participant.query.filter_by(event_id=event.id).count()
            participant = Participant(user=user, event=event)
            form.populate_obj(participant)
            participant.save_defaults()
            participant.status = PARTICIPANT_STATUS.PENDING if event.maximum_participants < total_participants else PARTICIPANT_STATUS.WL
            db.session.add(participant)
            db.session.commit()
            flash(u"Your request to participate has been recorded; you will be notified by the event manager", "success")
        else:
            return render_form(form=form, message=Markup(event.apply_instructions), 
                title="Participant Details", submit=u"Participate", 
                cancel_url=url_for('event_view', event=event.name,  
                profile=profile.name), ajax=False)
    # FIXME: Don't change anything unless this is a POST request
    elif participant.status == PARTICIPANT_STATUS.WITHDRAWN:
        participant.status = PARTICIPANT_STATUS.PENDING
        db.session.commit()
        flash(u"Your request to participate has been recorded; you will be notified by the event manager", "success")
    else:
        flash(u"Your request is pending", "error")
    return render_redirect(url_for('event_view', **values), code=303)


@app.route('/<profile>/<event>/withdraw', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_withdraw(profile, event):
    user_id = g.user.id
    participant = Participant.query.filter_by(event_id=event.id, user_id=user_id).first()
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

        form = ConfirmWithdrawForm()
        if form.validate_on_submit():
            if 'delete' in request.form:
                try:
                    withdraw_call[participant.status]()

                except KeyError:
                    pass

            db.session.commit()
            flash(u"Your request to withdraw from {0} is recorded".format(event.title), "success")
            values = {'profile': profile.name, 'event': event.name}
            return render_redirect(url_for('event_view', **values), code=303)
        return render_template('withdraw.html', form=form, title=u"Confirm withdraw",
            message=u"Withdraw from '%s' ? You can come back anytime." % (event.title))
    else:
        abort(404)


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
    # FIXME: Hardcoded state values. Unclear what calling them does
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
