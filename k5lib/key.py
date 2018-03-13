# Key management
# Documentation
# https://k5-doc.jp-east-1.paas.cloud.global.fujitsu.com/doc/en/iaas/document/api-reference/v2/mg/concept/title_part_002.html
#
"""
     {
        "endpoints": [
          {
            "interface": "public",
            "url": "https://keymanagement.fi-1.cloud.global.fujitsu.com/v1",
            "id": "0419c448001845af8f6828cf49745e72",
            "name": "keymanagement",
            "region_id": "fi-1",
            "region": "fi-1"
          }
        ],
        "id": "07f309b0ef9d42758ea4de47bdca9c32",
        "name": "keymanagement",
        "type": "keystore"
      },
      {
        "endpoints": [
          {
            "interface": "public",
            "url": "https://certificate.fi-1.cloud.global.fujitsu.com/v1",
            "id": "e1cc93936fb94cdbadc20f17c4ad3140",
            "name": "certificate",
            "region_id": "fi-1",
            "region": "fi-1"
          }
        ],
        "id": "0bd9a971e97d4c15af6b94311e4e9c15",
        "name": "certificate",
        "type": "certificate"
      },
"""
import requests
import json
import logging
import ipaddress
import datetime


def _create_key_container(project_token, region, az, project_id, container_type, container_name):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}
    """
    NOTE for SSL-VPN2
    The following fixed values must be specified for the key information container used when creating an SSL-VPN V2
    connection.

        type: It is necessary to specify "generic".
        name: It is necessary to specify "ca", "server_certificate", "server_key", and "dh".

    """

    valid_type = ['generic', 'certificate']
    if container_type not in valid_type:
        container_type = valid_type[0]

    configData ={
        "name": container_name,
        "type": container_type,
        "secret_refs":[]
    }

    url = 'https://keymanagement.' + region + '.cloud.global.fujitsu.com/v1/' + project_id +'/containers'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_key_container(project_token, region, az, project_id, container_type):

    request = _rest_create_key_container(project_token, region, az, project_id, container_type)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _create_key(project_token, region, az, project_id, container_type):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}


    valid_type = ['generic', 'certificate']
    if container_type not in valid_type:
        container_type = valid_type[0]

    configData = {'key1': {
                     'key2': [
                          {
                              'key3': 'value3'
                          }
                     ]
                 }
    }

    url = 'https://keymanagement.' + region + '.cloud.global.fujitsu.com/v1/' + project_id +'/secrets'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_key(project_token, region, az, project_id, container_type):

    request = _rest_create_key(project_token, region, az, project_id, container_type)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()

