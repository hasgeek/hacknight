# -*- coding: utf-8 -*-

from flask import render_template, g, abort, flash, url_for
from coaster.views import load_model, load_models
from baseframe.forms import render_redirect, render_form
from hacknight import app
from hacknight.models import db, Profile
from hacknight.models.event import profile_types, Event
from hacknight.forms.profile import ProfileForm
from hacknight.forms.event import EventForm
from hacknight.views.login import lastuser


@app.route('/<profile>')
@load_model(Profile, {'name': 'profile'}, 'profile')
def profile_view(profile):
    return render_template('profile.html', profile=profile)


@app.route('/<profile>/<event>', methods=["GET"])
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event'}, 'event'))
def event_view(profile, event):
    return render_template('event.html', event=event)

@app.route('/<profile>/new', methods=['GET', 'POST'])
@lastuser.requires_login
def event_new(profile):
    form = EventForm()
    if form.validate_on_submit():
        event = Event()
        form.populate_obj(event)
        event.make_name()
        db.session.add(event)
        db.session.commit()
        flash(u"You have created new event", "success")
        values={'profile': profile, 'event': event.name}
        return render_redirect(url_for('event_view', **values), code=303)
    return render_form(form=form, title="New Event", submit=u"Create",
        cancel_url=url_for('profile_view', profile=profile), ajax=False)


@app.route('/<profile>/<event>/edit', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_edit(profile, event):
    if not lastuser.has_permission('siteadmin') and event.profile.userid not in g.user.user_organization_ids():
        abort(403)
    form = EventForm(obj=event)
    if form.validate_on_submit():
        form.populate_obj(event)
        event.make_name()
        db.session.commit()
        flash(u"You have edited details for event %s" % event.title, "success")
        return render_redirect(url_for('event_view', event=event.name, profile=profile.name), code=303)
    return render_form(form=form, title="Edit Event", submit=u"Save",
        cancel_url=url_for('event_view', event=event.name), ajax=False)

@app.route('/<profile>/<event>/delete', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
  (Profile, {'name': 'profile'}, 'profile'),
  (Event, {'name': 'event', 'profile': 'profile'}, 'event'))
def event_delete(profile, event):
    if not lastuser.has_permission('siteadmin') and event.profile.userid not in g.user.user_organization_ids():
        abort(403)
    return render_delete_sqla(event, db, title=u"Confirm delete",
        message=u"Delete venue '%s'? This cannot be undone." % event.title,
        success=u"You have deleted playlist '%s'." % event.title,
         next=url_for('profile_view'))


@app.route('/<profile>/edit', methods=['GET', 'POST'])
@lastuser.requires_login
@load_model(Profile, {'name': 'profile'}, 'profile')
def profile_edit(profile):
    if profile.userid not in g.user.user_organization_ids():
        abort(403)
    form = ProfileForm(obj=profile)
    if profile.userid == g.user.userid:
        form.type.choices = [(1, profile_types[1])]
    else:
        choices = profile_types.items()
        choices.sort()
        choices.pop(0)
        choices.pop(0)
        form.type.choices = choices
    if form.validate_on_submit():
        form.populate_obj(profile)
        db.session.commit()
        flash(u"Edited description for profile", 'success')
        return render_redirect(url_for('profile_view', profile=profile.name), code=303)
    return render_form(form=form, title=u"Edit profile", submit=u"Save",
        cancel_url=url_for('profile_view', profile=profile.name), ajax=True)
