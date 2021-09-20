from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms.fields import StringField, SubmitField
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
app = Flask(__name__)
parameters = []


def float_check(form, field):
    try:
        float(field.data)
    except ValueError as e:
        raise ValidationError('Input should be float !')


class HppInputForm(FlaskForm):

    MSSubClass = StringField('MSSubClass', validators=[DataRequired(), float_check])
    LotArea = StringField('LotArea', validators=[DataRequired(), float_check])
    YearBuilt = StringField('YearBuilt', validators=[DataRequired(), float_check])
    BedroomAbvGr = StringField('BedroomAbvGr', validators=[DataRequired(), float_check])
    TotRmsAbvGrd = StringField('TotRmsAbvGrd', validators=[DataRequired(), float_check])

    predict = SubmitField('Submit Form')


@app.route("/")
def hello():
    logger.debug("Home page")
    return render_template("index.html")


# HPP Page
@app.route('/hpp_input', methods=['GET', 'POST'])
def hpp_input():
    form = HppInputForm()

    if form.predict.data and form.validate_on_submit():
        logger.debug("Processing user inputs")
        # hpp_prediction = [form.MSSubClass.data, form.YearBuilt.data, form.LotArea.data, form.BedroomAbvGr.data, form.TotRmsAbvGrd.data]
        parameters.clear()
        parameters.append(form.MSSubClass.data)
        parameters.append(form.YearBuilt.data)
        parameters.append(form.LotArea.data)
        parameters.append(form.BedroomAbvGr.data)
        parameters.append(form.TotRmsAbvGrd.data)
        logger.debug("User inputs taken")
        return render_template("display_prediction.html")
    return render_template("hpp_databroker.html", example_form=form)


def get_parameters():
    logger.debug("Return databroker parameters")
    return parameters


def app_run():
    app.secret_key = "hpp"
    bootstrap = Bootstrap(app)
    app.run(host="0.0.0.0", port=8062)
    # app.run()
