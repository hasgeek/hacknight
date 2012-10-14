# -*- coding: utf-8 -*-
from pytz import timezone
from dateutil import tz
from flask import render_template, abort, flash, url_for, g, request, Response
from coaster.views import load_model, load_models
from baseframe.forms import render_redirect, render_form, render_delete_sqla
from hacknight import app
from hacknight.models import db, Profile
from hacknight.models.event import Event
from hacknight.models.participant import Participant, PARTICIPANT_STATUS
from hacknight.models.project import ProjectMember, Project
from hacknight.forms.event import EventForm, ConfirmWithdrawForm
from hacknight.forms.participant import ParticipantForm
from hacknight.views.login import lastuser


@app.route('/<profile>/<event>', methods=["GET"])
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_view(profile, event):
    projects = Project.query.filter_by(event_id=event.id)
    participants = Participant.query.filter(
        Participant.status != PARTICIPANT_STATUS.WITHDRAWN,
        Participant.event == event)
    accepted_participants = [p for p in participants if p.status == PARTICIPANT_STATUS.CONFIRMED]
    accepted_participants_projects = dict((participant.user.fullname, None) for participant in accepted_participants)
    for p in accepted_participants:
        accepted_participants_projects[p.user.fullname] = ProjectMember.query.filter_by(participant_id=p.id).all()
    rest_participants = [p for p in participants if p.status != PARTICIPANT_STATUS.CONFIRMED]
    rest_participants_projects = dict((participant.user.fullname, None) for participant in rest_participants)
    for p in rest_participants:
        rest_participants_projects[p.user.fullname] = Project.query.filter_by(participant_id=p.id).all()
    applied = 0
    for p in participants:
        if p.user == g.user:
            applied = 1
            break
    current_participant = Participant.get(user=g.user, event=event) if g.user else None
    return render_template('event.html', profile=profile, event=event,
        projects=projects,
        accepted_participants_projects=accepted_participants_projects,
        rest_participants_projects=rest_participants_projects,
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
    if form.validate_on_submit():
        event = Event(profile=profile)
        form.populate_obj(event)
        if not event.name:
            event.make_name()
        """
            Datetime form is unaware of time zones.
            All the hacknights timings are in GMT for now, So convert the GMT timings
            to UTC and store in the DB.
        """
        local_zone = tz.gettz(app.config['TIMEZONE'])
        utc_zone = tz.gettz('UTC')
        event.start_datetime = event.start_datetime.replace(tzinfo=local_zone)
        # replace timezone info to GMT
        event.end_datetime = event.end_datetime.replace(tzinfo=local_zone)
        # convert timezone info to UTC
        event.start_datetime = event.start_datetime.astimezone(utc_zone)
        event.end_datetime = event.end_datetime.astimezone(utc_zone)
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
    local_zone = tz.gettz(app.config['TIMEZONE'])
    utc_zone = tz.gettz('UTC')
    # If the datetime object is unaware of timezone info replace with UTC time zone since all db entries are
    # converted to UTC and stored
    if not event.start_datetime.tzinfo:
        event.start_datetime = event.start_datetime.replace(tzinfo=utc_zone)
    if not event.end_datetime.tzinfo:
        event.end_datetime = event.end_datetime.replace(tzinfo=utc_zone)
    # Convert UTC to GMT
    event.start_datetime = event.start_datetime.astimezone(local_zone)
    event.end_datetime = event.end_datetime.astimezone(local_zone)
    # Note: Moving form initialization to top will not reflect the time conversion in edit form.
    form = EventForm(obj=event)
    if form.validate_on_submit():
        form.populate_obj(event)
        if not event.name:
            event.make_name()
        event.profile_id = profile.id
        event.start_datetime = event.start_datetime.replace(tzinfo=local_zone)
        event.end_datetime = event.end_datetime.replace(tzinfo=local_zone)
        event.start_datetime = event.start_datetime.astimezone(utc_zone)
        event.end_datetime = event.end_datetime.astimezone(utc_zone)
        """
        This is hack
        ------------

        SQLAlchemy compares the value of datetime object before storing to db. Newly entered values are
        timezone aware but values fetched from db aren't time aware. Previous state value is stored
        in `_sa_instance_state`. Injecting tzinfo, so that sqlalchemy understands how to compare the
        datetime object.
        """
        if not event._sa_instance_state.committed_state['start_datetime'].tzinfo:
            event._sa_instance_state.committed_state['start_datetime'] = event._sa_instance_state.committed_state['start_datetime'].replace(tzinfo=utc_zone)
        if not event._sa_instance_state.committed_state['end_datetime'].tzinfo:
            event._sa_instance_state.committed_state['end_datetime'] = event._sa_instance_state.committed_state['end_datetime'].replace(tzinfo=utc_zone)
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
        Participant.event == event)
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
            return render_form(form=form, title="Participant Details",
                submit=u"Participate", cancel_url=url_for('event_view',
                event=event.name, profile=profile.name), ajax=False)
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
