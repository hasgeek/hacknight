# -*- coding: utf-8 -*-

from flask import render_template, g, abort, flash, url_for
from coaster.views import load_models
from baseframe.forms import render_form, render_redirect, render_delete_sqla
from hacknight import app
from hacknight.views.login import lastuser
from hacknight.models import db, Profile, Event, Sponsor
from hacknight.forms.sponsor import SponsorForm


@app.route('/<profile>/<event>/sponsors/new', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    )
def sponsor_new(profile, event, form=None):
    if profile.userid not in g.user.user_organizations_owned_ids():
        abort(403)

    form = SponsorForm()
    if form.validate_on_submit():
        sponsor = Sponsor(event=event)
        form.populate_obj(sponsor)
        sponsor.make_name()
        db.session.add(sponsor)
        db.session.commit()
        flash("Sponsor added")
        return render_redirect(url_for('event_view', profile=profile.name,
        event=event.name), code=303)
    return render_form(form=form, title=u"New Sponsor", submit=u"Save",
        cancel_url=url_for('event_view', profile=profile.name,
            event=event.name), ajax=False)


@app.route('/<profile>/<event>/sponsors/<sponsor>/edit',
    methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Sponsor, {'name': 'sponsor', 'event': 'event'}, 'sponsor'),
    )
def sponsor_edit(profile, event, sponsor):
    if profile.userid not in g.user.user_organizations_owned_ids():
        abort(403)

    else:
        form = SponsorForm(obj=sponsor)
        if form.validate_on_submit():
            form.populate_obj(sponsor)
            db.session.commit()
            flash(u"Your changes have been saved", 'success')
            return render_redirect(url_for('sponsor_view',
                profile=profile.name, event=event.name, sponsor=sponsor.name), code=303)
        return render_form(form=form, title=u"Edit sponsor", submit=u"Save",
            cancel_url=url_for('sponsor_view', profile=profile.name, event=event.name,
                sponsor=sponsor.name), ajax=True)


@app.route('/<profile>/<event>/sponsors/<sponsor>/delete', methods=["GET", "POST"])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Sponsor, {'name':'sponsor', 'event':'event'}, 'sponsor'),
    )
def sponsor_delete(profile, event, sponsor):
    if not lastuser.has_permission('siteadmin') and profile.userid not in g.user.user_organizations_owned_ids():
        abort(403)

    return render_delete_sqla(sponsor, db, title=u"Confirm delete",
        message=u"Delete Sponsor '%s'? This cannot be undone." % sponsor.title,
        success=u"You have deleted the sponsor '%s'." % sponsor.title,
         next=url_for('event_view', profile=profile.name, event=event.name))


@app.route('/<profile>/<event>/sponsors/<sponsor>', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Sponsor, {'name': 'sponsor', 'event': 'event'}, 'sponsor'),
    )

def sponsor_view(profile, event, sponsor):
    return render_template('sponsor.html', sponsor=sponsor, profile=profile, event=event)
