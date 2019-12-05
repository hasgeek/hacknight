# -*- coding: utf-8 -*-

import wtforms
from coaster.utils import getbool
from baseframe.forms import Form, RichTextField

__all__ = ['ProjectForm']


class ProjectForm(Form):
    title = wtforms.TextField("Title", description="Title of the project", validators=[wtforms.validators.Required("A title is required"), wtforms.validators.length(max=250)])
    blurb = wtforms.TextField("Blurb", description="A single-line summary of the project",
        validators=[wtforms.validators.Required("A blurb is required"), wtforms.validators.length(max=250)])
    description = RichTextField("Description",
        description="Detailed description of your project",
        content_css="/static/css/editor.css")
    participating = wtforms.RadioField("Will you be participating?", default=1, coerce=getbool,
        choices=[(1, "I will be working on this project"),
                 (0, "I’m proposing an idea for others to take up")])
