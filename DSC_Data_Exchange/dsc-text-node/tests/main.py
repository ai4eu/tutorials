from resourceapi import ResourceApi
from idsapi import IdsApi
import requests
import pprint
import sys


providerUrl = "https://localhost:8080"
#consumerUrl = "https://localhost:8081"

#provider_alias = "https://provider-dataspace-connector"
#consumer_alias = "https://consumer-dataspace-connector"


def main(argv):
    if len(argv) == 2:
        provider_alias = argv[0]
        consumer_alias = argv[1]
        print("Setting provider alias as:", provider_alias)
        print("Setting consumer alias as:", consumer_alias)


if __name__ == "__main__":
    main(sys.argv[1:])

print("Starting script")

# Suppress ssl verification warning
requests.packages.urllib3.disable_warnings()

# Provider
provider = ResourceApi(providerUrl)

## Create resources
dataValue = "SOME LONG VALUE"
catalog = provider.create_catalog()
offers = provider.create_offered_resource()
representation = provider.create_representation()
artifact = provider.create_artifact(data={"value": dataValue})
contract = provider.create_contract()
use_rule = provider.create_rule()

## Link resources
provider.add_resource_to_catalog(catalog, offers)
provider.add_representation_to_resource(offers, representation)
provider.add_artifact_to_representation(representation, artifact)
provider.add_contract_to_resource(offers, contract)
provider.add_rule_to_contract(contract, use_rule)

print("Created provider resources")

# Consumer
#consumer = IdsApi(consumerUrl)

# Replace localhost references
#offers = offers.replace(providerUrl, provider_alias)
#artifact = artifact.replace(providerUrl, provider_alias)

# IDS
# Call description
#offer = consumer.descriptionRequest(provider_alias + "/api/ids/data", offers)
#pprint.pprint(offer)

# Negotiate contract
#obj = offer["ids:contractOffer"][0]["ids:permission"][0]
#obj["ids:target"] = artifact
#response = consumer.contractRequest(
#    provider_alias + "/api/ids/data", offers, artifact, False, obj
#)
#pprint.pprint(response)

# Pull data
#agreement = response["_links"]["self"]["href"]

#consumerResources = ResourceApi(consumerUrl)
#artifacts = consumerResources.get_artifacts_for_agreement(agreement)
#pprint.pprint(artifacts)

#first_artifact = artifacts["_embedded"]["artifacts"][0]["_links"]["self"]["href"]
#pprint.pprint(first_artifact)

#data = consumerResources.get_data(first_artifact).text
#pprint.pprint(data)

#if data != dataValue:
#    exit(1)

exit(0)
