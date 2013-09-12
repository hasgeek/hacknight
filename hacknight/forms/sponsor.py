# -*- coding: utf-8 -*-

import wtforms
import wtforms.fields.html5
from baseframe.forms import Form, RichTextField

__all__ = ['SponsorForm']


class SponsorForm(Form):
    title = wtforms.TextField("Title", description="Title of the project",
        validators=[wtforms.validators.Required("A title is required"), wtforms.validators.length(max=250)])
    description = RichTextField(u"Description",
        description="Detailed description of your project",
        content_css="/static/css/editor.css")
    website = wtforms.fields.html5.URLField("Home Page",
        description="URL to the home page", validators=[wtforms.validators.Optional(), wtforms.validators.length(max=250)])
    image_url = wtforms.fields.html5.URLField("Image URL", description="URL to the image",
        validators=[wtforms.validators.Required("An image is required."), wtforms.validators.length(max=250)])
