# -*- coding: utf-8 -*-

import flask.ext.wtf as wtf
from coaster import getbool
from baseframe.forms import Form, RichTextField

__all__ = ['ProjectForm']


class ProjectForm(Form):
    title = wtf.TextField("Title", description="Title of the project", validators=[wtf.Required("A title is required"), wtf.validators.length(max=250)])
    blurb = wtf.TextField("Blurb", description="A single-line summary of the project",
        validators=[wtf.Required("A blurb is required"), wtf.validators.length(max=250)])
    description = RichTextField(u"Description",
        description="Detailed description of your project",
        content_css="/static/css/editor.css")
    participating = wtf.RadioField("Will you be participating?", default=1, coerce=getbool,
        choices=[(1,  u"I will be working on this project"),
                 (0, u"I’m proposing an idea for others to take up")])
