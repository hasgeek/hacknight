# -*- coding: utf-8 -*-

import wtforms
import wtforms.fields.html5
from baseframe.forms import Form, RichTextField
from baseframe.staticdata import country_codes


__all__ = ['ParticipantForm', 'ExplaraForm']


class ParticipantForm(Form):
    skill_levels = [
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced')
    ]

    reason_to_join = RichTextField("Reason To Join",
        description="Why would you love to join Hacknight",
        validators=[wtforms.validators.Required()],
        content_css="/static/css/editor.css")
    phone_no = wtforms.TextField("Telephone No", description="Telephone No",
        validators=[wtforms.validators.Required(), wtforms.validators.length(max=15)])
    email = wtforms.fields.html5.EmailField("Email",
        description="Email Address, We will never spam you .",
        validators=[wtforms.validators.Required(), wtforms.validators.length(max=80)])
    job_title = wtforms.TextField("Job Title",
        description="What is your job title? E.G: Senior Software "
                    "Engineer at Awesome company",
        validators=[wtforms.validators.Optional(), wtforms.validators.length(max=120)])
    company = wtforms.TextField("Company", description="Company Name",
        validators=[wtforms.validators.Optional(), wtforms.validators.length(max=1200)])
    skill_level = wtforms.RadioField("Skill Level", description="What is your skill level?",
        choices=skill_levels)


class ExplaraForm(Form):
    name = wtforms.TextField("Name", description="Name of the purchaser",
        validators=[wtforms.validators.Required(), wtforms.validators.length(max=200)])
    email = wtforms.fields.html5.EmailField("Email", description="Email address",
         validators=[wtforms.validators.Required(), wtforms.validators.length(max=200)])
    phone_no = wtforms.TextField("Telephone No", description="Telephone No",
        validators=[wtforms.validators.Required(), wtforms.validators.length(max=15)])
    country = wtforms.SelectField("Country", description="Country", choices=country_codes, validators=[wtforms.validators.Required()])
    """ Longest state name
    Taumatawhakatangihangakoauauotamateahaumaitawhitiurehaeaturipuk-
    akapikimaungahoronukupokaiwhenuakitanatahu in NewZeland.
    """
    state = wtforms.TextField("State", description="State", validators=[wtforms.validators.Required(), wtforms.validators.length(max=110)])
    city = wtforms.TextField("City", description="City", validators=[wtforms.validators.Required(), wtforms.validators.length(max=110)])
    address = wtforms.TextField("Address", description="Address", validators=[wtforms.validators.Required(), wtforms.validators.length(max=1000)])
    zip_code = wtforms.TextField("Zip code", description="Zip code", validators=[wtforms.validators.Required(), wtforms.validators.length(max=6)])
