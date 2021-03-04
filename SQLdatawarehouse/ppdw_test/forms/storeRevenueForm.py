from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import InputRequired

class storeRevenueForm(FlaskForm):
    state = SelectField("State", choices=[], validators=[InputRequired()])
    submit = SubmitField("Generate Store Revenue Report")






