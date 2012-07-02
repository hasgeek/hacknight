# -*- coding: utf-8 -*-

import flask.ext.wtf as wtf
from baseframe.forms import Form, RichTextField

__all__ = ['ProfileForm']


class ProfileForm(Form):
    type = wtf.SelectField(u"Profile type", coerce=int, validators=[wtf.Required()])
    description = RichTextField(u"Description/Bio",
        content_css="/static/css/editor.css")
