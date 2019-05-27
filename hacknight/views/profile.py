# -*- coding: utf-8 -*-

from flask import render_template, g, abort, flash, request
from coaster.views import load_model
from baseframe.forms import render_redirect, render_form
from hacknight import app
from hacknight.models import db, Profile, User, Event, PROFILE_TYPE
from hacknight.models.event import profile_types
from hacknight.forms.profile import ProfileForm, NewsLetterForm
from hacknight.views.login import lastuser
from hacknight.models.participant import Participant


@app.route('/<profile>')
@load_model(Profile, {'name': 'profile'}, 'profile')
def profile_view(profile):
    events = Event.query.filter_by(profile_id=profile.id).order_by(Event.start_datetime.desc()).all()
    user = User.query.filter_by(userid=profile.userid).first()
    if user is not None:
        # User profile. Show all events this user owns or is participating in.
        events = list(set(events + [p.event for p in Participant.query.filter_by(user=user).all()]))
        events.sort(key=lambda item: item.start_datetime, reverse=True)
    return render_template('profile.html.jinja2', profile=profile, events=events, is_user=True if user else False)


@app.route('/<profile>/edit', methods=['GET', 'POST'])
@lastuser.requires_login
@load_model(Profile, {'name': 'profile'}, 'profile')
def profile_edit(profile):
    if profile.userid not in g.user.user_organizations_owned_ids():
        abort(403)
    form = ProfileForm(obj=profile)
    # FIXME: The way "choices" are populated is very confusing. Make this clearer.
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
        return render_redirect(profile.url_for(), code=303)
    return render_form(form=form, title=u"Edit profile", submit=u"Save",
        cancel_url=profile.url_for(), ajax=True)


@app.route('/<profile>/settings', methods=['POST', 'GET'])
@lastuser.requires_login
@load_model(Profile, {'name': 'profile'}, 'profile')
def profile_settings(profile):
    user = g.user
    if not user.profile == profile:
        return render_redirect(user.profile.url_for('settings'))
    form = NewsLetterForm(obj=user)
    action = request.args.get('action')
    if action == "unsubscribe":
        form.send_newsletter.data = False
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        flash(u"Newsletter preference for '{fullname}' is saved".format(fullname=user.fullname), 'success')
        return render_redirect(profile.url_for(), code=303)
    return render_form(form=form, title=u"Settings", submit=u"Save",
        cancel_url=profile.url_for(), ajax=False)
