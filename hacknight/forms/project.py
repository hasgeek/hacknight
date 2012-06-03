# -*- coding: utf-8 -*-

import flask.ext.wtf as wtf
from baseframe.forms import Form, RichTextField

__all__ = ['ProjectForm']


class ProjectForm(Form):
    name = wtf.TextField('Name', validators=[wtf.Required('A name is required')])
    title = wtf.TextField('Title', validators=[wtf.Required('A title is required')])
    description = RichTextField(u"Description")
    status = wtf.RadioField("Are you hacking?", coerce=int,
        choices=[(0, u"I would like to be involved in this project."),
                 (0, u"I’m proposing for someone else to take it up.")])

