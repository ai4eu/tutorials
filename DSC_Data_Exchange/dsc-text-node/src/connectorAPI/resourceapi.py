#
# Copyright 2020 Fraunhofer Institute for Software and Systems Engineering
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import requests
import json

# Suppress ssl verification warning
requests.packages.urllib3.disable_warnings()


class ResourceApi:
    session = None
    recipient = None

    def __init__(self, recipient, auth=("admin", "password")):
        self.session = requests.Session()
        self.session.auth = auth
        self.session.verify = False

        self.recipient = recipient

    def create_catalog(self, data={}):
        response = self.session.post(self.recipient + "/api/catalogs", json=data)
        return response.headers["Location"]

    def create_offered_resource(self, data={}):
        response = self.session.post(self.recipient + "/api/offers", json=data)
        return response.headers["Location"]

    def create_representation(self, data={}):
        response = self.session.post(self.recipient + "/api/representations", json=data)
        return response.headers["Location"]

    def create_artifact(self, data={"value": "SOME LONG VALUE"}):
        response = self.session.post(self.recipient + "/api/artifacts", json=data)
        return response.headers["Location"]

    def update_artifact(self, artifact, data) -> bool:
        response = self.session.put(artifact, json=data)
        return response.status_code == 204

    def create_contract(
        self,
        data={
            "start": "2021-04-06T13:33:44.995+02:00",
            "end": "2021-12-06T13:33:44.995+02:00",
        },
    ):
        response = self.session.post(self.recipient + "/api/contracts", json=data)
        return response.headers["Location"]

    def create_rule(
        self,
        data={
            "value": """{
            "@context" : {
                "ids" : "https://w3id.org/idsa/core/",
                "idsc" : "https://w3id.org/idsa/code/"
            },
            "@type": "ids:Permission",
            "@id": "https://w3id.org/idsa/autogen/permission/cf1cb758-b96d-4486-b0a7-f3ac0e289588",
            "ids:action": [
                {
                "@id": "idsc:USE"
                }
            ],
            "ids:description": [
                {
                "@value": "provide-access",
                "@type": "http://www.w3.org/2001/XMLSchema#string"
                }
            ],
            "ids:title": [
                {
                "@value": "Example Usage Policy",
                "@type": "http://www.w3.org/2001/XMLSchema#string"
                }
            ]
            }"""
        },
    ):
        response = self.session.post(self.recipient + "/api/rules", json=data)
        return response.headers["Location"]

    def add_resource_to_catalog(self, catalog, resource):
        return self.session.post(
            catalog + "/offers", json=self.toListIfNeeded(resource)
        )

    def add_catalog_to_resource(self, resource, catalog):
        return self.session.post(
            resource + "/catalogs", json=self.toListIfNeeded(catalog)
        )

    def add_representation_to_resource(self, resource, representation):
        return self.session.post(
            resource + "/representations", json=self.toListIfNeeded(representation)
        )

    def add_artifact_to_representation(self, representation, artifact):
        return self.session.post(
            representation + "/artifacts", json=self.toListIfNeeded(artifact)
        )

    def add_contract_to_resource(self, resource, contract):
        return self.session.post(
            resource + "/contracts", json=self.toListIfNeeded(contract)
        )

    def add_rule_to_contract(self, contract, rule):
        return self.session.post(contract + "/rules", json=self.toListIfNeeded(rule))

    def toListIfNeeded(self, obj):
        if isinstance(obj, list):
            return obj
        else:
            return [obj]

    def get_data(self, artifact):
        return self.session.get(artifact + "/data")

    def get_artifacts_for_agreement(self, agreement):
        return json.loads(self.session.get(agreement + "/artifacts").text)
