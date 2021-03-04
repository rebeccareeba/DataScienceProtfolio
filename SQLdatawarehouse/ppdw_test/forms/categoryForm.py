from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import InputRequired


class categoryForm(FlaskForm):
    year = SelectField("Year", choices=[], validators=[InputRequired()])
    month = SelectField("Month", choices=[], validators=[InputRequired()])
    submit = SubmitField("Generate Category Report")

