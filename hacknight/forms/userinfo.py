# -*- coding: utf-8 -*-

import flask.ext.wtf as wtf
from baseframe.forms import Form, RichTextField

__all__ = ['UserInfoForm']


class UserInfoForm(Form):
    phone_no = wtf.html5.TelField("Telephone No", description="Telephone No", validators=[wtf.Required()])
    reason_to_join = RichTextField("Reason To Join", description="Why would you love to join Hacknight", validators=[wtf.Required()])
    email = wtf.html5.EmailField("Email", description="Email Address, We will never spam you .", validators=[wtf.Required()])
    job_title = wtf.TextField("Job Title", description="What is your job title? E.G: Senior Software Engineer at Awesome company",
                              validators=[wtf.Required()])
    company = wtf.TextField("Company", description="Company Name", validators=[wtf.Optional()])