# -*- coding: utf-8 -*-

from flask import render_template, g, abort, flash, url_for, request
from coaster.views import load_model, load_models
from baseframe.forms import render_form, render_redirect, ConfirmDeleteForm
from hacknight import app
from hacknight.models import db, Profile, Event, Project, ProjectMember, Participant
from hacknight.models.event import profile_types
from hacknight.forms.project import ProjectForm
from hacknight.views.login import lastuser


@app.route('/<profile>/<event>/new', methods=['GET', 'POST'])
@load_models((Event, {'name': 'event'}, 'event'),
    (Profile, {'name':'profile'}, 'profile'))
@lastuser.requires_login
def project_new(profile, event, form=None):
    if request.method=="GET":
        if form == None:
            form = ProjectForm()
            return render_form(form=form, title=u"New Project", submit=u"Save",
        cancel_url=url_for('index'), ajax=True)
    
    if request.method=="POST":
        form = ProjectForm()
        project = Project()
        form.populate_obj(project)
        project.make_name()
        project.profile_id = g.user
        project.event_id = event.id 
        db.session.add(project)
        db.session.commit()
        project_member = ProjectMember()
        project_member.project_id = project.id
        project_member.participant_id = Participant.query.filter_by(user_id=g.user.id).first().id
        db.session.add(project_member)
        db.session.commit()
        flash("Project saved")
        return render_redirect(url_for('index'), code=303)


@app.route('/<profile>/<event>/projects/<project>/edit', methods=['GET', 'POST'])
@load_models((Profile, {'name':'profile'}, 'profile'),
    (Project, {'name': 'project'}, 'project'),
    (Event, {'name':'event'}, 'event'))
@lastuser.requires_login
def project_edit(profile, project, event):
    if g.user not in project.users:
        abort(403)
    else:
        form = ProjectForm(obj=project)
        if form.validate_on_submit():
            form.populate_obj(project)
            db.session.commit()
            flash(u"Your changes have been saved", 'success')
            return render_redirect(url_for('index'), code=303)
        return render_form(form=form, title=u"Edit project", submit=u"Save",
            cancel_url=url_for('index'), ajax=True)

@app.route('/<profile>/<event>/projects/<project>/remove', methods=["GET", "POST"])
@load_models((Profile, {'name':'profile'}, 'profile'),
    (Project, {'name': 'project'}, 'project'),
    (Event, {'name':'event'}, 'event'))
@lastuser.requires_login
def project_remove(profile, project, event):
    if not lastuser.has_permission('siteadmin') and g.user not in project.users:
        abort(403)
    else:
        form = ConfirmDeleteForm()
    if form.validate_on_submit():
        if 'delete' in request.form:
            members = ProjectMember.query.filter_by(project_id=project.id).all()
            print members
            for member in members:
                db.session.delete(member)
            db.session.delete(project)
            db.session.commit()
            flash("Project removed", "success")
        return render_redirect(url_for('index'), code=303)
    return render_template('baseframe/delete.html', form=form, title=u"Confirm delete",
        message=u"Delete '%s' ?" % (project.title))


@app.route('/<profile>/<event>/projects', methods=["GET","POST"])
@load_models((Profile, {'name':'profile'}, 'profile'),
    (Event, {'name':'event'}, 'event'))
def projects(profile, event):
    projects = Project.query.filter_by(event_id=event.id)
    return render_template('projects.html', projects=projects, event=event)

