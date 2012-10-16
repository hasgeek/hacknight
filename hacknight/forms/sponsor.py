# -*- coding: utf-8 -*-

import flask.ext.wtf as wtf
from baseframe.forms import Form, RichTextField

__all__ = ['SponsorForm']


class SponsorForm(Form):
    title = wtf.TextField("Title", description="Title of the project",
        validators=[wtf.Required("A title is required")])
    description = RichTextField(u"Description",
        description="Detailed description of your project",
        content_css="/static/css/editor.css")
    website = wtf.html5.URLField("Home Page",
        description="URL to the home page", validators=[wtf.Optional()])
    image_url = wtf.html5.URLField("Image URL", description="URL to the image",
        validators=[wtf.Required("An image is required.")])
