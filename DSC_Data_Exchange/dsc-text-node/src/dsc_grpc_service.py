from src.connectorAPI.idsapi import IdsApi
from src.connectorAPI.resourceapi import ResourceApi


def get_text(conf):
    consumer_url = conf.custom_dsc if conf.use_custom_dsc else "https://localhost:8080"
    consumer = IdsApi(consumer_url)

    response = consumer.contractRequest(
        conf.provider_url_downloading, conf.resource_id, conf.artifact_id, False, conf.contract
    )

    agreement = response["_links"]["self"]["href"]
    consumer_resources = ResourceApi(consumer_url)
    artifacts = consumer_resources.get_artifacts_for_agreement(agreement)
    first_artifact = artifacts["_embedded"]["artifacts"][0]["_links"]["self"]["href"]
    data = consumer_resources.get_data(first_artifact).text
    print(data)

    return data
