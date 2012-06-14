# -*- coding: utf-8 -*-

import flask.ext.wtf as wtf
from baseframe.forms import Form, RichTextField

__all__ = ['ProjectForm']


class ProjectForm(Form):
    title = wtf.TextField('Title', description="Title of the project", validators=[wtf.Required('A title is required')])

    description = RichTextField(u"Description", description="Describe your project with supporting links to datasets or other preperatory material. Also say why you want to work on it.")
    status = wtf.RadioField("Are you hacking?",default=0, coerce=int,
        choices=[(0, u"I will be working on this project"),
                 (1, u"I’m proposing to invite someone to take it up")])

