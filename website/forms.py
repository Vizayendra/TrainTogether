from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField, StringField, DateField, TimeField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    receiver = SelectField('Send To', coerce=int, validators=[DataRequired()])
    content = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')


class ActivityForm(FlaskForm):
    activity_type = SelectField(
        'Activity Type',
        choices=[
            ('', '-- Select an activity --'),
            ('running', 'Running'),
            ('swimming', 'Swimming'),
            ('yoga', 'Yoga'),
            ('cycling', 'Cycling'),
            ('gym', 'Gym Workout')
        ],
        validators=[DataRequired(message="Please select an activity")]
    )
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Add Activity')
