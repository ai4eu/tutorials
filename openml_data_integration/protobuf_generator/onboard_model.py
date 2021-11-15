#!/usr/bin/env python3
# =============================================================================
# Copyright (C) 2019 Fraunhofer Gesellschaft. All rights reserved.
# =============================================================================
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
# ===============LICENSE_END===================================================

import requests
import os
import json
import numpy as np
from utils import *
import openml

# setup parameters
acumos_host = os.environ['ACUMOS_HOST'] # FQHN like aiexp-preprod.ai4europe.eu
registry_host = os.environ['REGISTRY_HOST']
token = os.environ['ACUMOS_TOKEN'] # format is 'acumos_username:API_TOKEN'
user = os.environ['ACUMOS_USER']
psw = os.environ['ACUMOS_PW']
catalog_id = os.environ['ACUMOS_CATALOGID']
docker_base = f'{registry_host}:7444/ai4eu-experiments/openml'

header_type = {
    "Content-Type": "application/json"
}
foder_prefix = 'openml_'


def update_data(api, data, headers, post_req=True):    
    if post_req:
        update_response = requests.post(api, 
                    auth=(user, psw),
                    headers=headers,
                    data=json.dumps(data)                    
                )
    else:
        if headers: # for not image
            # get data first
            get_response = requests.get(api, auth=(user, psw))    
            if get_response.status_code!=200: 
                print(f'Fail to get data! Error code: {get_response.status_code}')
                return False
        
            get_data = json.loads(get_response.text)
            # update data
            get_data.update(data)
            data = json.dumps(get_data)
        update_response = requests.put(api, 
                                    auth=(user, psw),
                                    headers=headers,
                                    data=data
                                )
    if update_response.status_code!=200:
        print(f'Fail: {update_response.status_code}')
        print(f'Response Text: {update_response.text}')
        return False   
    return True


def set_authors_publisher(solution_id, revision_id, dataset_id):
    author_api = f'https://{acumos_host}/ccds/solution/{solution_id}/revision/{revision_id}'
    with open(f'{foder_prefix}{dataset_id}/authors.txt') as f:
        authors = ''.join(f.readlines())     
    
    if authors == 'None': authors = 'OpenML'
    data = {
        "authors": [{
            "name": authors,
            "contact": "www.openml.org"
            }],
        "publisher": "OpenML"
    }
    return update_data(author_api, data, headers=header_type, 
                            post_req=False)            



def set_description(revision_id, dataset_id):    
    desc_api = f'https://{acumos_host}/ccds/revision/{revision_id}/catalog/{catalog_id}/descr'    
    with open(f'{foder_prefix}{dataset_id}/description.txt') as f:
        desc = ''.join(f.readlines())
    data = {
        "description": desc        
    }
    return update_data(desc_api, data, headers=header_type, 
                            post_req=True)    


def set_tags(solution_id):    
    tag_api = f'https://{acumos_host}/ccds/solution/{solution_id}'
    data = {
        "modelTypeCode": "DS",
        "toolkitTypeCode": "SK",
        "tags": [
            {
                "tag": "OpenML"
            }
        ]
    }
    reponse = update_data(tag_api, data=data, 
                        headers=header_type,
                        post_req=False)
    if reponse:
        tag_api = f'https://{acumos_host}/ccds/catalog/{catalog_id}/solution/{solution_id}'
        return update_data(tag_api, data=data, 
                        headers=header_type,
                        post_req=True)
    return False


def set_icon(solution_id, dataset_id):
    icon_api = f'https://{acumos_host}/ccds/solution/{solution_id}/pic'
    path_img = f'{foder_prefix}{dataset_id}/icon.png'    
    with open(path_img, 'rb') as img:
        return update_data(icon_api, data=img.read(),
                                headers=None, 
                                post_req=False) 


def get_revision_id(solution_id):
    
    revision_api = f'https://{acumos_host}/ccds/solution/{solution_id}/revision'
    response = requests.get(revision_api, 
                    auth=(user, psw)
                )
    if response.status_code == 200:
        body = json.loads(response.text)
        version = np.array([i['version'] for i in body]).argmax()        
        return body[version]['revisionId']
    else:
        print(f'Can not get Revision ID. Error code: {response.status_code}')
        return 0



def onboarding(model_name, dockerImageURI, dataset_id):
    license_file = "./license-1.0.0.json"
    protobuf_file = "./model.proto"    
    # setup parameters
    advanced_api = "https://" + acumos_host + ":443/onboarding-app/v2/advancedModel"
    files= {'license': ('license.json', 
                        open(f'{foder_prefix}{dataset_id}/{license_file}', 'rb'), 
                        'application.json'),
            'protobuf': ('model.proto', 
                        open(f'{foder_prefix}{dataset_id}/{protobuf_file}', 'rb'), 
                        'text/plain')}
    headers = {
        "Accept": "application/json",
        "modelname": model_name,
        "Authorization": token,
        "dockerFileURL": dockerImageURI,
        'isCreateMicroservice': 'false'
        }

    #send request
    response = requests.post(advanced_api, files=files, headers=headers)

    #check response
    if response.status_code == 201:
        body = json.loads(response.text)
        solution_id = body['result']['solutionId']
        print("Docker uri is pushed successfully on {" + acumos_host + "}, response is: ", 
                    response.status_code, " - solutionId: ", solution_id, '\n')
        return solution_id
    
    print("Docker uri is not pushed on {" + acumos_host + "}, response is: ", 
                                                    response.status_code, '\n')
    return 0


def main():
    OpenMLFiles = get_file_Nums_of_interest()
    for dataset_id in OpenMLFiles:
        model_name = openml.datasets.get_dataset(dataset_id).name
        dockerImageURI = os.path.join(docker_base, f'{model_name}_{dataset_id}:v1')
        solution_id = onboarding(model_name, dockerImageURI, dataset_id)
        if solution_id!=0:
            # get the latest revision_id
            revision_id = get_revision_id(solution_id)
            if revision_id!=0:
                status = set_authors_publisher(solution_id, revision_id, dataset_id)
                print(f'Authors+Publisher Update: {"Successful" if status else "Fail"}')
                status = set_description(revision_id, dataset_id)
                print(f'Description Update: {"Successful" if status else "Fail"}')
                status = set_tags(solution_id)
                print(f'Tag Update: {"Successful" if status else "Fail"}')
                status = set_icon(solution_id, dataset_id)
                print(f'Icon Update: {"Successful" if status else "Fail"}')


if __name__ == '__main__':
    main()
