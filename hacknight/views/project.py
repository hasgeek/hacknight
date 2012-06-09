# -*- coding: utf-8 -*-

from flask import render_template, g, abort, flash, url_for, request, redirect
from coaster.views import load_model, load_models
from baseframe.forms import render_form, render_redirect, ConfirmDeleteForm
from hacknight import app
from hacknight.models import db, Profile, Event, Project, ProjectMember, Participant
from hacknight.models.event import profile_types
from hacknight.forms.project import ProjectForm
from hacknight.forms.comment import CommentForm, DeleteCommentForm, ConfirmDeleteForm
from hacknight.views.login import lastuser
from hacknight.models.vote import VoteSpace, Vote
from hacknight.models.comment import Comment, CommentSpace
from markdown import Markdown

markdown = Markdown(safe_mode="escape").convert

@app.route('/<profile>/<event>/new', methods=['GET', 'POST'])
@load_models((Event, {'name': 'event'}, 'event'),
	(Profile, {'name':'profile'}, 'profile'))
@lastuser.requires_login
def project_new(profile, event, form=None):
	if request.method=="GET":
		if form == None:
			form = ProjectForm()
			return render_form(form=form, title=u"New Project", submit=u"Save",
		cancel_url=url_for('index'), ajax=False)
	
        if request.method=="POST":
            form = ProjectForm()
            project = Project()
            votespace = VoteSpace()
            votespace.type= 0
            commentspace = CommentSpace()
            db.session.add(commentspace)
            db.session.add(votespace)
            db.session.commit()
            form.populate_obj(project)
            project.votes = votespace
            project.comments = commentspace
            project.comment_id = commentspace.id
            project.make_name()
            project.event_id = event.id
            project.votes_id = votespace.id
            project.votes.vote(g.user)
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

@app.route('/<profile>/<event>/projects/<project>', methods=["GET","POST"])
@load_models((Profile, {'name':'profile'}, 'profile'),
	(Project, {'name': 'project'}, 'project'),
	(Event, {'name':'event'}, 'event'))
def project_show(profile,project,event):
    if not event:
        abort(404)
    if not project:
        abort(404)

    comments = sorted(Comment.query.filter_by(commentspace=project.comments, parent=None).order_by('created_at').all(),
        key=lambda c: c.votes.count, reverse=True)
    commentform = CommentForm()
    delcommentform = DeleteCommentForm()
    if request.method == 'POST':
        print "here"
        if request.form.get('form.id') == 'newcomment' and commentform.validate():
            if commentform.edit_id.data:
                comment = Comment.query.get(int(commentform.edit_id.data))
                if comment:
                    if comment.user == g.user:
                        comment.message = commentform.message.data
                        comment.message_html = markdown(comment.message)
                        comment.edited_at = datetime.utcnow()
                        flash("Your comment has been edited", "info")
                    else:
                        flash("You can only edit your own comments", "info")
                else:
                    flash("No such comment", "error")
            else:
                comment = Comment(user=g.user, commentspace=project.comments, message=commentform.message.data)
                if commentform.parent_id.data:
                    parent = Comment.query.get(int(commentform.parent_id.data))
                    if parent and parent.commentspace == proposal.comments:
                        comment.parent = parent
                comment.message_html = markdown(comment.message)
                project.comments.count += 1
                comment.votes.vote(g.user)  # Vote for your own comment
                db.session.add(comment)
                flash("Your comment has been posted", "info")
            db.session.commit()
            # Redirect despite this being the same page because HTTP 303 is required to not break
            # the browser Back button
            return redirect(url_for('project_show',profile=profile.name, project=project.name, event=event.name))

        elif request.form.get('form.id') == 'delcomment' and delcommentform.validate():
            comment = Comment.query.get(int(delcommentform.comment_id.data))
            if comment:
                if comment.user == g.user:
                    comment.delete()
                    proposal.comments.count -= 1
                    db.session.commit()
                    flash("Your comment was deleted.", "info")
                else:
                    flash("You did not post that comment.", "error")
            else:
                flash("No such comment.", "error")
            return redirect(url_for('project_show',profile=profile.name, project=project.name, event=event.name))
    return render_template('project_show.html', event=event, project=project, profile=profile,
        comments=comments, commentform=commentform, delcommentform=delcommentform,
        breadcrumbs=[(url_for('index'), "home")])


@app.route('/<profile>/<event>/projects/<project>/voteup')
@load_models((Profile, {'name':'profile'}, 'profile'),
    (Project, {'name': 'project'}, 'project'),
    (Event, {'name':'event'}, 'event'))
@lastuser.requires_login
def voteupsession(profile, project,event):
    if not event:
        abort(404)
    if not project:
        abort(404)
    project.votes.vote(g.user, votedown=False)
    db.session.commit()
    flash("Your vote has been recorded", "info")
    return redirect(url_for('project_show',profile=profile.name, project=project.name, event=event.name))


# FIXME: This voting method uses GET but makes db changes. Not correct. Should be POST
@app.route('/<profile>/<event>/projects/<project>/votedown')
@load_models((Profile, {'name':'profile'}, 'profile'),
    (Project, {'name': 'project'}, 'project'),
    (Event, {'name':'event'}, 'event'))
@lastuser.requires_login
def votedownsession(profile, project,event):
    if not event:
        abort(404)
    if not project:
        abort(404)
    project.votes.vote(g.user, votedown=True)
    db.session.commit()
    flash("Your vote has been recorded", "info")
    return redirect(url_for('project_show',profile=profile.name, project=project.name, event=event.name))


# FIXME: This voting method uses GET but makes db changes. Not correct. Should be POST
@app.route('/<profile>/<event>/projects/<project>/cancelvote')
@load_models((Profile, {'name':'profile'}, 'profile'),
    (Project, {'name': 'project'}, 'project'),
    (Event, {'name':'event'}, 'event'))
@lastuser.requires_login
def votecancelsession(profile, project, event):
    if not event:
        abort(404)
    if not project:
        abort(404)
    project.votes.cancelvote(g.user)
    db.session.commit()
    flash("Your vote has been withdrawn", "info")
    return redirect(url_for('project_show',profile=profile.name, project=project.name, event=event.name))

@app.route('/<profile>/<event>/projects/<project>/comments/<int:cid>/voteup')
@load_models((Profile, {'name':'profile'}, 'profile'),
    (Project, {'name': 'project'}, 'project'),
    (Event, {'name':'event'}, 'event'),
    (Comment, {'id':'cid'}, 'comment'))
@lastuser.requires_login
def voteupcomment(profile, project, event, comment):
    if not event:
        abort(404)
    if not project:
        abort(404)
    if not comment:
        abort(404)
    comment.votes.vote(g.user, votedown=False)
    db.session.commit()
    flash("Your vote has been recorded", "info")
    return redirect(url_for('project_show',profile=profile.name, project=project.name, event=event.name))


# FIXME: This voting method uses GET but makes db changes. Not correct. Should be POST
@app.route('/<profile>/<event>/projects/<project>/comments/<int:cid>/votedown')
@load_models((Profile, {'name':'profile'}, 'profile'),
    (Project, {'name': 'project'}, 'project'),
    (Event, {'name':'event'}, 'event'),
    (Comment, {'id':'cid'}, 'comment'))
@lastuser.requires_login
def votedowncomment(profile, project, event, comment):
    if not event:
        abort(404)
    if not project:
        abort(404)
    if not comment:
        abort(404)
    comment.votes.vote(g.user, votedown=True)
    db.session.commit()
    flash("Your vote has been recorded", "info")
    return redirect(url_for('project_show',profile=profile.name, project=project.name, event=event.name))


# FIXME: This voting method uses GET but makes db changes. Not correct. Should be POST
@app.route('/<profile>/<event>/projects/<project>/comments/<int:cid>/cancelvote')
@load_models((Profile, {'name':'profile'}, 'profile'),
    (Project, {'name': 'project'}, 'project'),
    (Event, {'name':'event'}, 'event'),
    (Comment, {'id':'cid'}, 'comment'))
@lastuser.requires_login
def votecancelcomment(profile, project, event, comment):
    if not event:
        abort(404)
    if not project:
        abort(404)
    if not comment:
        abort(404)
    comment.votes.cancelvote(g.user)
    db.session.commit()
    flash("Your vote has been withdrawn", "info")
    return redirect(url_for('project_show',profile=profile.name, project=project.name, event=event.name))


@app.route('/<profile>/<event>/projects/<project>/next')
@load_models((Profile, {'name':'profile'}, 'profile'),
    (Project, {'name': 'project'}, 'project'),
    (Event, {'name':'event'}, 'event'))
def nextsession(profile, project, event):
    if not event:
        abort(404)
    if not project:
        abort(404)

    next = project.getnext()
    if next:
        return redirect(url_for('project_show',profile=profile.name, project=next.name, event=event.name))
    else:
        flash("You were at the last proposal", "info")
        return redirect(url_for('project_show',profile=profile.name, project=project.name, event=event.name))


@app.route('/<profile>/<event>/projects/<project>/prev')
@load_models((Profile, {'name':'profile'}, 'profile'),
    (Project, {'name': 'project'}, 'project'),
    (Event, {'name':'event'}, 'event'))
def prevsession(profile, project, event):
    if not event:
        abort(404)
    if not project:
        abort(404)

    prev = project.getprev()
    if prev:
        return redirect(url_for('project_show',profile=profile.name, project=prev.name, event=event.name))
    else:
        flash("You were at the first proposal", "info")
        return redirect(url_for('project_show',profile=profile.name, project=project.name, event=event.name))

