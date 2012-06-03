# -*- coding: utf-8 -*-

from flask import render_template, g, abort, flash, url_for, request
from coaster.views import load_model
from baseframe.forms import render_redirect, render_form
from hacknight import app
from hacknight.models import db, Profile, Event, Project
from hacknight.models.event import profile_types
from hacknight.forms.project import ProjectForm
from hacknight.views.login import lastuser


@app.route('/<event>/new', methods=['GET', 'POST'])
@load_model(Event, {'name': 'event'}, 'event')
@lastuser.requires_login
def project_new(event, form=None):
	if request.method=="GET":
		if form == None:
			form = ProjectForm()
			return render_form(form=form, title=u"New Project", submit=u"Save",
        cancel_url=url_for('index'), ajax=True)
	
	if request.method=="POST":
		form = ProjectForm()
		project = Project()
		form.populate_obj(project)
		project.event_id = event.id
        db.session.add(project)
        db.session.commit()
        flash("Project saved")
        return render_redirect(url_for('index'), code=303)
