import os.path
import pprint

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from src.dsc_grpc_service import get_text
from src.state.configuration_state import Configuration, get_jsonifyed_configuration

template_dir = os.path.abspath('templates')
app = Flask(__name__, template_folder=template_dir)
ma = Marshmallow(app)
conf = None


class HppInputForm(FlaskForm):
    recipient_str = StringField('Recipient', validators=[DataRequired(), ])
    resource_id_str = StringField('Resource Id', validators=[DataRequired(), ])
    artifact_id_str = StringField('Artifact Id', validators=[DataRequired(), ])
    contract_input_str = StringField('Contract', validators=[DataRequired(), ])

    custom_consumer_toggle = BooleanField('Use Custom Consumer')
    custom_consumer_str = StringField('Custom Consumer')

    submit = SubmitField('Submit Configuration')


class PullForm(FlaskForm):
    submit = SubmitField('Pull Data')


@app.route('/api/v1/recipient', methods=["POST"])
def set_recipient():
    print('------------')
    print("set recipient to: ")
    pprint.pprint(request.get_json()['recipient'])
    print('------------')
    conf.recipient = request.get_json()['recipient']
    pprint.pprint(conf.recipient)
    return get_jsonifyed_configuration()


@app.route('/api/v1/resourceId', methods=["POST"])
def set_resource_id():
    print('------------')
    print("set resourceId to: ")
    pprint.pprint(request.get_json()['resourceId'])
    print('------------')
    conf.resource_id = request.get_json()['resourceId']
    return get_jsonifyed_configuration()


@app.route('/api/v1/artifactId', methods=["POST"])
def set_artifact_id():
    print('------------')
    print("set artifactId to: ")
    pprint.pprint(request.get_json()['artifactId'])
    print('------------')
    conf.artifact_id = request.get_json()['artifactId']
    return get_jsonifyed_configuration()


@app.route('/api/v1/download', methods=["POST"])
def set_download():
    print('------------')
    print("set download to: ")
    pprint.pprint(request.get_json()['download'])
    print('------------')
    conf.download = request.get_json()['download']
    return get_jsonifyed_configuration()


@app.route('/api/v1/contract', methods=["POST"])
def set_contract():
    print('------------')
    print("set contract to: ")
    pprint.pprint(request.get_json()['contract'])
    print('------------')
    conf.contract = request.get_json()['contract']
    return get_jsonifyed_configuration()


@app.route('/api/v1/useCustomDSC', methods=["POST"])
def set_use_custom_dsc():
    print('------------')
    print("set useCustomDSC to: ")
    pprint.pprint(request.get_json()['useCustomDSC'])
    print('------------')
    conf.use_custom_dsc = request.get_json()['useCustomDSC']
    return get_jsonifyed_configuration()


@app.route('/api/v1/data', methods=["GET"])
def get_data():
    data = get_text(conf)
    print('------------')
    print("Sending Data: ")
    print(data)
    print('------------')
    return data


@app.route('/api/v1/customDSC', methods=["POST"])
def set_custom_dsc():
    print('------------')
    print("set customDSC to: ")
    pprint.pprint(request.get_json()['customDSC'])
    print('------------')
    conf.custom_dsc = request.get_json()['customDSC']
    return get_jsonifyed_configuration()


@app.route('/', methods=["GET", "POST"])
@app.route('/hpp_input', methods=["GET", "POST"])
def index():
    form = HppInputForm()
    pull_form = PullForm()

    if pull_form.submit.data and pull_form.validate_on_submit():
        return render_template("index.html", form=form, data=get_text(conf), current_configuration=Configuration(),
                               pull_form=pull_form)

    if form.submit.data and form.validate_on_submit():
        print('processing User Input')
        conf.recipient = form.recipient_str.data
        conf.resource_id = form.resource_id_str.data
        conf.artifact_id = form.artifact_id_str.data
        conf.contract = form.contract_input_str.data
        conf.use_custom_dsc = form.custom_consumer_toggle.data
        conf.custom_dsc = form.custom_consumer_str.data

        return render_template("index.html", form=form, current_configuration=Configuration(), pull_form=pull_form)

    return render_template('index.html', form=form, current_configuration=Configuration(), pull_form=pull_form)


def run_flask_app(host: str, port: int, p_conf):
    global conf
    conf = p_conf
    print("--------------------------------------")
    print("--------------------------------------")
    print("starting flask server")
    print("--------------------------------------")
    print("--------------------------------------")
    print(conf)

    app.secret_key = "dscmodel"
    bootstrap = Bootstrap(app)
    app.app_context().push()
    app.run(host=host, port=port)
