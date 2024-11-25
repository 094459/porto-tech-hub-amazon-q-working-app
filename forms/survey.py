from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FieldList, SubmitField, RadioField
from wtforms.validators import DataRequired, Length

class CreateSurveyForm(FlaskForm):
    title = StringField('Survey Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    options = FieldList(StringField('Option', validators=[DataRequired()]), min_entries=2, max_entries=5)
    submit = SubmitField('Create Survey')

class SurveyResponseForm(FlaskForm):
    option = RadioField('Select your response', validators=[DataRequired()])
    email = StringField('Email (optional)', validators=[Length(max=100)])