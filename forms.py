from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import Required

class ContactForm(FlaskForm):
    subject = StringField("Subject", validators=[Required()])
    message = TextAreaField("Message", validators=[Required()])
    submit = SubmitField("Send")


class CommentForm(FlaskForm):
    body = TextAreaField('', validators=[Required()])
    submit = SubmitField('Submit')
