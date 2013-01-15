import flask.ext.wtf as wtf
from baseframe.forms import Form, RichTextField

__all__ = ['ParticipantForm']


class ParticipantForm(Form):
    skill_levels = [
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Advanced', 'Advanced')
    ]

    reason_to_join = RichTextField("Reason To Join",
        description="Why would you love to join Hacknight",
        validators=[wtf.Required()],
        content_css="/static/css/editor.css")
    phone_no = wtf.TextField("Telephone No", description="Telephone No",
        validators=[wtf.Required(), wtf.validators.length(max=15)])
    email = wtf.html5.EmailField("Email",
        description="Email Address, We will never spam you .",
        validators=[wtf.Required(), wtf.validators.length(max=80)])
    job_title = wtf.TextField("Job Title",
        description="What is your job title? E.G: Senior Software "
                    "Engineer at Awesome company",
        validators=[wtf.Optional(), wtf.validators.length(max=120)])
    company = wtf.TextField("Company", description="Company Name",
        validators=[wtf.Optional(), wtf.validators.length(max=1200)])
    skill_level = wtf.RadioField("Skill Level", description="What is your skill level?",
        choices=skill_levels)
