# -*- coding: utf-8 -*-

from flask import render_template, abort, flash, url_for, g, request, Response, redirect
from coaster.views import load_model, load_models
from baseframe.forms import render_redirect, render_form, render_delete_sqla
from hacknight import app
from hacknight.models import db, Profile, User
from hacknight.models.event import Event, EventStatus
from hacknight.models.participant import Participant, ParticipantStatus
from hacknight.models.project import Project
from hacknight.models.venue import Venue
from hacknight.forms.event import EventForm, ConfirmWithdrawForm
from hacknight.forms.participant import ParticipantForm
from hacknight.views.login import lastuser
import hacknight.views.workflow


@app.route('/<profile>/<event>', methods=["GET"])
@load_models((Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_view(profile, event):
    if not profile:
        abort(404)
    if not event:
        abort(404)

    projects = Project.query.filter_by(event_id=event.id)
    participants = Participant.query.filter(
        Participant.status != ParticipantStatus.OWNER).filter(
        Participant.status != ParticipantStatus.WITHDRAWN).filter(
        Participant.event == event)

    acceptedP = [p for p in participants if p.status == ParticipantStatus.CONFIRMED]
    restP = [p for p in participants if p.status != ParticipantStatus.CONFIRMED]
    applied = 0
    owner = 0
    for p in participants:
        if p.user == g.user:
            applied = 1
            break
    if g.user:
        user = User.query.filter_by(userid=g.user.userid).first()
        if user.profile == profile:
            owner = 1

    return render_template('event.html', profile=profile, event=event,
        projects=projects, venue=Venue.query.filter_by(id=event.venue_id).first(), timezone=event.start_datetime.strftime("%Z"),
        acceptedparticipants=acceptedP, restparticipants=restP, applied=applied, owner=owner)


@app.route('/<profile>/new', methods=['GET', 'POST'])
@lastuser.requires_login
@load_model(Profile, {'name': 'profile'}, 'profile')
def event_new(profile):
    form = EventForm()
    #venues = Venue.query.filter(Venue.profile_id.in_([p.id for p in g.user.profiles])).all()
    #venues hold list of venues created by organization members to list in drop down
    form.venue_id.choices = [(venue.id, venue.name) for venue in Venue.query.all()]
    if form.validate_on_submit():
        event = Event()
        form.populate_obj(event)
        if Event.query.filter_by(name=event.name, profile=profile).first():
            flash("Event name %s already exists." % event.title, "fail")
            return render_form(form=form, title="New Event", submit=u"Create",
                cancel_url=url_for('profile_view', profile=profile.name), ajax=False)
        event.make_name()
        event.profile_id = profile.id
        db.session.add(event)
        db.session.commit()

        participant = Participant(user_id=g.user.id, event_id=event.id, status=ParticipantStatus.OWNER)
        db.session.add(participant)
        db.session.commit()
        flash(u"New event created", "success")
        values = {'profile': profile.name, 'event': event.name}
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
    #venues = Venue.query.filter(Venue.profile_id.in_([p.id for p in g.user.profiles])).all()
    #venues hold list of venues created by organization members to list in drop down
    form.venue_id.choices = [(venue.id, venue.name) for venue in Venue.query.all()]
    if form.validate_on_submit():
        form.populate_obj(event)
        event.make_name()
        event.profile_id = profile.id
        db.session.commit()
        flash(u"Your edits to %s are saved" % event.title, "success")
        return render_redirect(url_for('event_view', event=event.name, profile=profile.name), code=303)
    return render_form(form=form, title="Edit Event", submit=u"Save",
        cancel_url=url_for('event_view', event=event.name, profile=profile.name), ajax=False)



participant_status_labels = {
    ParticipantStatus.PENDING: "Pending",
    ParticipantStatus.WL: "Waiting List",
    ParticipantStatus.CONFIRMED: "Confirmed",
    ParticipantStatus.REJECTED: "Rejected",
    ParticipantStatus.WITHDRAWN: "Withdrawn",
    ParticipantStatus.OWNER: "Owner"
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
    if  profile.userid not in g.user.user_organization_owned_ids():
        abort(403)
    participants = Participant.query.filter(
        Participant.status != ParticipantStatus.WITHDRAWN,
        Participant.status != ParticipantStatus.OWNER,
        Participant.event == event)
    return render_template('manage_event.html', profile=profile, event=event,
        participants=participants, statuslabels=participant_status_labels)


@app.route('/<profile>/<event>/manage/update', methods=['POST'])
@lastuser.requires_login
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_update_participant_status(profile, event):
    if  profile.userid not in g.user.user_organization_owned_ids():
        return Response("Forbidden", 403)
    participantid = int(request.form['participantid'])
    status = int(request.form['status'])
    participant = Participant.query.get(participantid)

    if(participant.event != event):
        return Response("Forbidden", 403)
    if(participant.status == ParticipantStatus.WITHDRAWN):
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
    user_id = g.user.id
    participant = Participant.query.filter_by(event_id=event.id, user_id=user_id).first()
    if not participant:
        # If no participant is found create a new participant entry
        # First collect some information about the new participant
        user = g.user
        form = ParticipantForm(obj=user)
        if form.validate_on_submit():
            total_participants = Participant.query.filter_by(event_id=event.id).count()
            participant = Participant()
            form.populate_obj(participant)
            participant.user = user
            participant.event = event
            participant.save_defaults()
            participant.status = ParticipantStatus.PENDING if event.maximum_participants < total_participants else ParticipantStatus.WL
            db.session.add(participant)
            db.session.commit()
        else:
            flash(u"Your request to participate is recorded, you will be notified by the event manager".format(g.user.fullname, event.title), "success")
            return render_form(form=form, title="Participant Details",
                submit=u"Participate", cancel_url=url_for('event_view',
                event=event.name, profile=profile.name), ajax=False)
    elif participant.status == ParticipantStatus.WITHDRAWN:
        participant.status = ParticipantStatus.PENDING
        db.session.commit()
        flash(u"Your request to participate is recorded, you will be notified by the event manager".format(g.user.fullname, event.title), "success")
    else:
        flash(u"Your request is pending. ", "error")
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

        form = ConfirmWithdrawForm()
        if form.validate_on_submit():
            if 'delete' in request.form:
                try:
                    withdraw_call[participant.status]()

                except KeyError:
                    pass

            db.session.commit()
            flash(u"Your request to withdraw from {0} is recorded".format(event.title), "success")
            values={'profile': profile.name, 'event': event.name}
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
