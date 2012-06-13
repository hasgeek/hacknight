# -*- coding: utf-8 -*-

from flask import render_template, g, abort, flash, url_for
from coaster.views import load_model, load_models
from baseframe.forms import render_redirect, render_form
from hacknight import app
from hacknight.models import db, Profile, User
from hacknight.models.event import profile_types
from hacknight.forms.profile import ProfileForm
from hacknight.views.login import lastuser
from markdown import markdown
from hacknight.models.participant import Participant

@app.route('/<profile>')
@load_model(Profile, {'name': 'profile'}, 'profile')
def profile_view(profile):
    user = User.query.filter_by(userid=profile.userid).first()
    participants = Participant.query.filter_by(user_id=user.id).all()
    events = []
    for participant in participants:
        events.append(participant.event)
    return render_template('profile.html', profile=profile,events=events ,description=markdown(profile.description, safe_mode='escape'))


@app.route('/<profile>/edit', methods=['GET', 'POST'])
@lastuser.requires_login
@load_model(Profile, {'name': 'profile'}, 'profile')
def profile_edit(profile):
    if profile.userid not in g.user.user_organization_owned_ids():
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
