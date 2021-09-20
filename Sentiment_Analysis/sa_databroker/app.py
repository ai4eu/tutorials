from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from wtforms import validators
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
app = Flask(__name__)
query_list = []


class SAInputForm(FlaskForm):
    Query = StringField('Query', [validators.Length(min=4, max=25), validators.DataRequired()])
    predict = SubmitField('Submit Query')


@app.route("/")
def hello():
    logger.debug("Home page")
    return render_template("index.html")


# HPP Page
@app.route('/sa_input', methods=['GET', 'POST'])
def hpp_input():
    form = SAInputForm()

    if form.predict.data and form.validate_on_submit():
        logger.debug("Processing user query")
        query_list.clear()
        query_list.append(form.Query.data)
        logger.debug("User inputs taken")
        return render_template("display_prediction.html")
    return render_template("sa_databroker.html", example_form=form)


def get_query():
    logger.debug("Return databroker parameters")
    return query_list[0]


def app_run():
    app.secret_key = "sa"
    bootstrap = Bootstrap(app)
    app.run(host="0.0.0.0", port=8062)
    # app.run()
