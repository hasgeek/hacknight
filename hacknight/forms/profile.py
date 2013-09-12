# -*- coding: utf-8 -*-

import wtforms
from baseframe.forms import Form, RichTextField

__all__ = ['ProfileForm']


class ProfileForm(Form):
    type = wtforms.SelectField(u"Profile type", coerce=int, validators=[wtforms.validators.Required()])
    description = RichTextField(u"Description/Bio",
        content_css="/static/css/editor.css")
