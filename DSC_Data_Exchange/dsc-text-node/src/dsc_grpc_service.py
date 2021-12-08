import pprint

from src.connectorAPI.idsapi import IdsApi
from src.connectorAPI.resourceapi import ResourceApi


def get_text(conf):
    pprint.pprint("recipient: " + conf.recipient)
    pprint.pprint("use_custom_dsc: " + str(conf.use_custom_dsc))
    pprint.pprint("contract: " + str(conf.contract))
    pprint.pprint("resource_id: " + conf.resource_id)
    pprint.pprint("artifact_id: " + conf.artifact_id)
    pprint.pprint("custom_dsc: " + conf.custom_dsc)

    consumer_url = conf.custom_dsc if conf.use_custom_dsc else "https://localhost:8080"
    consumer = IdsApi(consumer_url)

    response = consumer.contractRequest(
        conf.recipient, conf.resource_id, conf.artifact_id, False, conf.contract
    )

    agreement = response["_links"]["self"]["href"]
    consumer_resources = ResourceApi(consumer_url)
    artifacts = consumer_resources.get_artifacts_for_agreement(agreement)
    first_artifact = artifacts["_embedded"]["artifacts"][0]["_links"]["self"]["href"]
    data = consumer_resources.get_data(first_artifact).text
    print(data)

    return data
