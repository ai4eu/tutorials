import flask


class Configuration:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Configuration, cls).__new__(cls)
        return cls.instance

    recipient = None
    resource_id = None
    artifact_id = None
    contract = None
    custom_dsc = None

    download = True
    use_custom_dsc = False

    data_send = False


def get_jsonifyed_configuration():
    return flask.jsonify({
        "recipient": Configuration().recipient,
        "resource_id": Configuration().resource_id,
        "artifact_id": Configuration().artifact_id,
        "download": Configuration().download,
        "contract": Configuration().contract,
        "use_custom_dsc": Configuration().use_custom_dsc,
        "custom_dsc": Configuration().custom_dsc,
    })
