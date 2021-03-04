from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.fields.html5 import DateField
from wtforms.validators import InputRequired


class HolidayForm(FlaskForm):
    holiday_date = DateField("Holiday Date", validators=[InputRequired()], format='%Y-%m-%d')
    holiday_name = StringField("Holiday Name(s)", validators=[InputRequired()])
    submit = SubmitField("Add Holiday")
