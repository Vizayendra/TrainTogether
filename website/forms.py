from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField, StringField, DateField, TimeField
from wtforms.validators import DataRequired

class MessageForm(FlaskForm):
    receiver = SelectField('Send To', coerce=int, validators=[DataRequired()])
    content = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')
