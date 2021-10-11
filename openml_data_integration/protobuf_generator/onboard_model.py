#!/usr/bin/env python3
# ===================================================================================
# Copyright (C) 2019 Fraunhofer Gesellschaft. All rights reserved.
# ===================================================================================
# This Acumos software file is distributed by Fraunhofer Gesellschaft
# under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ===============LICENSE_END==========================================================
"""
Provides an example of Docker URI cli on-boarding
"""
import requests
import os
import json

# properties of the model
model_name = "my-model-1"
dockerImageURI = "cicd.ai4eu-dev.eu:7444/myimages/onboardingtest:v3" #Docker image URI looks like: example.com:port/image-tag:version
license_file = "./license-1.0.0.json"
protobuf_file = "./model.proto"

# setup parameters
host = os.environ['ACUMOS_HOST'] # FQHN like aiexp-preprod.ai4europe.eu
token = os.environ['ACUMOS_TOKEN'] # format is 'acumos_username:API_TOKEN'
advanced_api = "https://" + host + ":443/onboarding-app/v2/advancedModel"
files= {'license': ('license.json', open(license_file, 'rb'), 'application.json'),
        'protobuf': ('model.proto', open(protobuf_file, 'rb'), 'text/plain')}
headers = {"Accept": "application/json",
           "modelname": model_name,
           "Authorization": token,
           "dockerFileURL": dockerImageURI,
           'isCreateMicroservice': 'false'}

#send request
response = requests.post(advanced_api, files=files, headers=headers)

#check response
if response.status_code == 201:
    body = json.loads(response.text)
    solution_id = body['result']['solutionId']
    print("Docker uri is pushed successfully on {" + host + "}, response is: ", response.status_code, " - solutionId: ", solution_id)
else:
    print("Docker uri is not pushed on {" + host + "}, response is: ", response.status_code)
