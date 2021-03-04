from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import InputRequired


class CityForm(FlaskForm):
    population = StringField("City Population", validators=[InputRequired()])
    submit = SubmitField("Update City Population")
