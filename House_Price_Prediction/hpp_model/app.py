from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms.fields import StringField, SubmitField
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
app = Flask(__name__)


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

    predict = SubmitField('Predict House Price')


@app.route("/")
def hello():
    time.sleep(5)
    results = []
    with open("results.txt", mode="r") as f:
        for line in f.readlines():
            result = line.replace("\n", "").split("|")
            results.append(result)
        f.close()
    results.reverse()
    headers = ['MSSubClass', 'LotArea', 'YearBuilt', 'BedroomAbvGr', 'TotRmsAbvGrd', 'SalePrice']
    return render_template("index.html", headers=headers, results=results)


# if __name__ == '__main__':
def app_run():
    app.secret_key = "hppmodel"
    bootstrap = Bootstrap(app)
    app.run(host="0.0.0.0", port=8062)
    # app.run()
