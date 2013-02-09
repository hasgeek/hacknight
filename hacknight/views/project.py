# -*- coding: utf-8 -*-

import unicodecsv
from cStringIO import StringIO
from datetime import datetime
from flask.ext.mail import Message
from flask import render_template, g, abort, flash, url_for, request, redirect, make_response
from coaster.views import load_models, jsonp
from baseframe.forms import render_form, render_redirect, ConfirmDeleteForm
from hacknight import app
from hacknight.models import db, Profile, Event, Project, ProjectMember, Participant, PARTICIPANT_STATUS
from hacknight.forms.project import ProjectForm
from hacknight.forms.comment import CommentForm, DeleteCommentForm
from hacknight.views.login import lastuser
from hacknight.views.event import send_email
from hacknight.models.vote import Vote
from hacknight.models.comment import Comment
from markdown import Markdown
import bleach

markdown = Markdown(safe_mode="escape").convert


@app.route('/<profile>/<event>/new', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    )
def project_new(profile, event, form=None):
    participant = Participant.get(user=g.user, event=event)
    if participant == None:
        abort(403)
    if participant.status != PARTICIPANT_STATUS.CONFIRMED:
        abort(403)

    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(event=event, user=g.user)
        form.populate_obj(project)
        project.make_name()
        db.session.add(project)
        project.votes.vote(g.user)

        project_member = ProjectMember(project=project, user=g.user)
        db.session.add(project_member)
        db.session.commit()
        flash("Project saved")
        return render_redirect(url_for('project_view', profile=profile.name, event=event.name, project=project.url_name))
    return render_form(form=form, title=u"New Project", submit=u"Save",
        cancel_url=url_for('event_view', profile=profile.name, event=event.name), ajax=False)


@app.route('/<profile>/<event>/projects/<project>/edit', methods=['GET', 'POST'])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Project, {'url_name': 'project', 'event': 'event'}, 'project')
    )
def project_edit(profile, project, event):
    if g.user not in project.users:
        abort(403)
    else:
        form = ProjectForm(obj=project)
        if request.method == 'GET':
            form.participating.data = str(int(project.participating))
        if form.validate_on_submit():
            form.populate_obj(project)
            project.make_name()
            db.session.commit()
            flash(u"Your changes have been saved", 'success')
            return render_redirect(url_for('project_view', profile=profile.name, event=event.name,
                project=project.url_name), code=303)
        return render_form(form=form, title=u"Edit project", submit=u"Save",
            cancel_url=url_for('project_view', profile=profile.name, event=event.name,
                project=project.url_name), ajax=False)


@app.route('/<profile>/<event>/projects/<project>/delete', methods=["GET", "POST"])
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Project, {'url_name': 'project', 'event': 'event'}, 'project')
    )
def project_delete(profile, project, event):
    if not lastuser.has_permission('siteadmin') and g.user not in project.users:
        abort(403)
    form = ConfirmDeleteForm()
    if form.validate_on_submit():
        if 'delete' in request.form:
            # FIXME: All of this should cascade. No need to delete one at a time
            members = ProjectMember.query.filter_by(project_id=project.id).all()
            comments = Comment.query.filter_by(commentspace=project.comments).all()
            votes = Vote.query.filter_by(votespace=project.votes).all()
            for comment in comments:
                db.session.delete(comment)
            for vote in votes:
                db.session.delete(vote)
            for member in members:
                db.session.delete(member)
            db.session.delete(project.comments)
            db.session.delete(project.votes)
            db.session.delete(project)
            db.session.commit()
            flash("Project removed", "success")
            return render_redirect(url_for('event_view', profile=profile.name, event=event.name), code=303)
    return render_template('baseframe/delete.html', form=form, title=u"Confirm delete",
        message=u"Delete '%s' ? It will remove comments, votes and all information related to the project. This operation cannot be undone." % (project.title))


@app.route('/<profile>/<event>/projects', methods=["GET", "POST"])
def projects(profile, event):
    return redirect(url_for('event_view', profile=profile, event=event))


@app.route('/<profile>/<event>/projects/<project>', methods=["GET", "POST"])
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Project, {'url_name': 'project', 'event': 'event'}, 'project'))
def project_view(profile, event, project):
    user_is_member = False
    if g.user:
        project_member = ProjectMember.query.filter_by(project_id=project.id, user_id=g.user.id).first()
        project_members = ProjectMember.query.filter_by(project_id=project.id).all()
        if project_members:
            email_ids = [member.user.email for member in project_members]
        if project_member:
            user_is_member = True
    # Fix the join query below and replace the cascaded if conditions.
    # if g.user:
    #   query = (ProjectMember
    #       .query.filter(ProjectMember.project_id == project.id)
    #       .join(Participant).filter(Participant.event_id == event.id)
    #       .join(User).filter(User.userid == g.user.userid))
    #   print "user id = %s, event id = %s, project id = %s" % (
    #       g.user.userid, event.id, project.id)
    #   print query.statement
    #   project_member = query.first()
    #   print project_member.project.name

    comments = sorted(Comment.query.filter_by(commentspace=project.comments, reply_to=None).order_by('created_at').all(),
        key=lambda c: c.votes.count, reverse=True)
    commentform = CommentForm()
    delcommentform = DeleteCommentForm()
    commentspace = project.comments
    if request.method == 'POST':
        if request.form.get('form.id') == 'newcomment' and commentform.validate():
            if commentform.edit_id.data:
                comment = commentspace.get_comment(int(commentform.edit_id.data))
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
                send_email_info = []
                if commentform.reply_to_id.data:
                    reply_to = commentspace.get_comment(int(commentform.reply_to_id.data))
                    if reply_to and reply_to.commentspace == project.comments:
                        comment.reply_to = reply_to
                        if not reply_to.user == g.user:
                            send_email_info.append({"to": reply_to.email,
                                "subject": "Hacknight: %s " % (project.title),
                                "template": 'project_team_email.md'})
                        email_ids.remove(project.user.email)
                        send_email_info.append({"to": project.user.email,
                                "subject": "Hacknight: %s " % (project.title),
                                "template": 'project_owner_email.md'})
                        email_ids.remove(g.user.email)
                        for email_id in email_ids:
                            send_email_info.append({"to": email_id,
                            "subject": "Hacknight: %s " % (project.title),
                            "template": 'project_team_email.md'})
                else:
                    if not g.user == project.user.email:
                        email_ids.remove(project.user.email)
                        send_email_info.append({"to": project.user.email,
                            "subject": "Hacknight: %s " % (project.title),
                            "template": 'project_owner_email.md'})
                    email_ids.remove(g.user.email)
                    for email_id in email_ids:
                        send_email_info.append({"to": email_id,
                            "subject": "Hacknight: %s " % (project.title),
                            "template": 'project_team_email.md'})

                comment.message_html = bleach.linkify(markdown(commentform.message.data))
                project.comments.count += 1
                comment.votes.vote(g.user)  # Vote for your own comment
                comment.make_id()
                db.session.add(comment)
                flash("Your comment has been posted", "info")
            db.session.commit()
            link = url_for('project_view', profile=profile.name, event=event.name,
                project=project.url_name, _external=True) + "#c" + str(comment.id)
            for item in send_email_info:
                email_body = render_template(item.pop('template'), project=project, comment=comment, link=link)
                send_email(sender=(g.user.fullname, g.user.email), html=markdown(email_body), body=email_body, **item)
            # Redirect despite this being the same page because HTTP 303 is required to not break
            # the browser Back button
            return redirect(url_for('project_view', profile=profile.name, event=event.name, project=project.url_name))

        elif request.form.get('form.id') == 'delcomment' and delcommentform.validate():
            comment = commentspace.get_comment(int(delcommentform.comment_id.data))
            if comment:
                if comment.user == g.user:
                    comment.delete()
                    project.comments.count -= 1
                    db.session.commit()
                    flash("Your comment was deleted.", "info")
                else:
                    flash("You did not post that comment.", "error")
            else:
                flash("No such comment.", "error")
            return redirect(url_for('project_view', profile=profile.name, event=event.name, project=project.url_name))
    return render_template('project.html', event=event, project=project, profile=profile,
        comments=comments, commentform=commentform, delcommentform=delcommentform,
        breadcrumbs=[(url_for('index'), "home")], user_is_member=user_is_member)


@app.route('/<profile>/<event>/projects/<project>/voteup')
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Project, {'url_name': 'project', 'event': 'event'}, 'project'))
def project_voteup(profile, project, event):
    if not event:
        abort(404)
    if not project:
        abort(404)
    project.votes.vote(g.user, votedown=False)
    db.session.commit()
    flash("Your vote has been recorded", "info")
    return redirect(url_for('project_view', profile=profile.name, event=event.name, project=project.url_name))


# FIXME: This voting method uses GET but makes db changes. Not correct. Should be POST
@app.route('/<profile>/<event>/projects/<project>/votedown')
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Project, {'url_name': 'project', 'event': 'event'}, 'project'))
def project_votedown(profile, event, project):
    if not event:
        abort(404)
    if not project:
        abort(404)
    project.votes.vote(g.user, votedown=True)
    db.session.commit()
    flash("Your vote has been recorded", "info")
    return redirect(url_for('project_view', profile=profile.name, event=event.name, project=project.url_name))


# FIXME: This voting method uses GET but makes db changes. Not correct. Should be POST
@app.route('/<profile>/<event>/projects/<project>/cancelvote')
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Project, {'url_name': 'project', 'event': 'event'}, 'project'))
def project_cancelvote(profile, project, event):
    if not event:
        abort(404)
    if not project:
        abort(404)
    project.votes.cancelvote(g.user)
    db.session.commit()
    flash("Your vote has been withdrawn", "info")
    return redirect(url_for('project_view', profile=profile.name, event=event.name, project=project.url_name))


@app.route('/<profile>/<event>/projects/<project>/comments/<int:cid>/voteup')
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Project, {'url_name': 'project', 'event': 'event'}, 'project'),
    (Comment, {'url_id': 'cid', 'commentspace': 'project.comments'}, 'comment'))
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
    return redirect(url_for('project_view', profile=profile.name, event=event.name, project=project.url_name))


# FIXME: This voting method uses GET but makes db changes. Not correct. Should be POST
@app.route('/<profile>/<event>/projects/<project>/comments/<int:cid>/votedown')
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Project, {'url_name': 'project', 'event': 'event'}, 'project'),
    (Comment, {'url_id': 'cid', 'commentspace': 'project.comments'}, 'comment'))
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
    return redirect(url_for('project_view',profile=profile.name, project=project.url_name, event=event.name))

@app.route('/<profile>/<event>/projects/<project>/comments/<int:cid>/json')
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Project, {'url_name': 'project', 'event': 'event'}, 'project'),
    (Comment, {'url_id': 'cid', 'commentspace': 'project.comments'}, 'comment'))
def jsoncomment(profile, project, event, comment):
    if not event:
        abort(404)
    if not project:
        abort(404)
    if not comment:
        abort(404)

    # comment = Comment.query.get(cid)
    if comment:
        return jsonp(message=comment.message)
    else:
        return jsonp(message='')


# FIXME: This voting method uses GET but makes db changes. Not correct. Should be POST
@app.route('/<profile>/<event>/projects/<project>/comments/<int:cid>/cancelvote')
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Project, {'url_name': 'project', 'event': 'event'}, 'project'),
    (Comment, {'url_id': 'cid', 'commentspace': 'project.comments'}, 'comment'))
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
    return redirect(url_for('project_view',profile=profile.name, project=project.url_name, event=event.name))


@app.route('/<profile>/<event>/projects/<project>/next')
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Project, {'url_name': 'project', 'event': 'event'}, 'project'))
def nextsession(profile, project, event):
    if not event:
        abort(404)
    if not project:
        abort(404)

    next = project.getnext()
    if next:
        return redirect(url_for('project_view',profile=profile.name, project=next.url_name, event=event.name))
    else:
        flash("You were at the last project", "info")
        return redirect(url_for('project_view',profile=profile.name, project=project.url_name, event=event.name))


@app.route('/<profile>/<event>/projects/<project>/prev')
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Project, {'url_name': 'project', 'event': 'event'}, 'project'))
def prevsession(profile, project, event):
    if not event:
        abort(404)
    if not project:
        abort(404)

    prev = project.getprev()
    if prev:
        return redirect(url_for('project_view',profile=profile.name, project=prev.url_name, event=event.name))
    else:
        flash("You were at the first project", "info")
        return redirect(url_for('project_view',profile=profile.name, project=project.url_name, event=event.name))

@app.route('/<profile>/<event>/projects/<project>/join')
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    (Project, {'url_name': 'project', 'event': 'event'}, 'project'))
def project_join(profile, project, event):
    participant = Participant.query.filter_by(user=g.user, event=event, status=PARTICIPANT_STATUS.CONFIRMED).first()
    if participant==None:
        flash("You need to be a confirmed participant to join this team.", "fail")
        return redirect(url_for('project_view',profile=profile.name, project=project.url_name, event=event.name))
    elif ProjectMember.query.filter_by(project_id=project.id, user=g.user).first():
        flash("You are already part of this team!", "fail")
    else:
        project_member = ProjectMember()
        project_member.project_id = project.id
        project_member.user_id = g.user.id
        db.session.add(project_member)
        db.session.commit()
        flash("You are now part of this team!", "success")
        return redirect(url_for('project_view',profile=profile.name, project=project.url_name, event=event.name))
    return redirect(url_for('project_view',profile=profile.name, project=project.url_name, event=event.name))


@app.route('/<profile>/<event>/export')
@lastuser.requires_login
@load_models(
    (Profile, {'name': 'profile'}, 'profile'),
    (Event, {'name': 'event', 'profile': 'profile'}, 'event'),
    )
def event_export(profile, event):
    if profile.userid not in g.user.user_organizations_owned_ids():
        abort(403)

    participants = StringIO()
    fieldnames = ['Ticket Number', 'Name', 'Email', 'Ticket Type', 'Company', 'Job', 'City', 'Twitter', 'Tshirt', 'Date', 'Order ID', "Skill Level", 'Phone No']
    writer = unicodecsv.DictWriter(participants, fieldnames=fieldnames, delimiter=',', quotechar='|', quoting=unicodecsv.QUOTE_MINIMAL)
    writer.writeheader()
    for p in event.participants:
        if p.status == PARTICIPANT_STATUS.CONFIRMED:
            writer.writerow({"Ticket Number": p.id,
            "Name": p.user.fullname,
            "Email": p.email,
            "Ticket Type": "Regular",
            "Company": p.company,
            "Job": p.job_title,
            "City": "",
            "Twitter": "",
            "Tshirt": "",
            "Date": p.created_at,
            "Order ID": "",
            "Skill Level": p.skill_level,
            "Phone No": p.phone_no
            })
    response = make_response(participants.getvalue())
    response.headers['Content-Type'] = 'text/csv;charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename=participants.csv'
    return response
