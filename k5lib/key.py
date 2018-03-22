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

log = logging.getLogger(__name__)


def _rest_create_key_container(project_token, region, project_id, container_type, container_name, key_list):
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
        "secret_refs": key_list
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


def create_key_container(project_token, region, project_id, container_type, container_name, key_list):
    """
    Create a key container.
    :param project_token: Valid K5 project token
    :param region: Valid K5 region
    :param project_id: Project ID
    :param container_type: Type of the container. Valid values are:  'certificate', 'generic' (str)
    :param container_name: Name of the containe (str)
    :param key_list: List of dictionaries.
        ::
        example:
         [
             {
                 "name": "private_key",
                 "secret_ref":"http://<host>:9311/v1/a759452216fd41cf8ee5aba321cfbd49/secrets/087cf096-3947-4a54-8968-7b021cfe8196"
             },
             {
                 "name": "certificate",
                 "secret_ref":"http://<host>:9311/v1/a759452216fd41cf8ee5aba321cfbd49/secrets/4bbcf05f-d15d-444c-ae9f-799746349a9f"
             },
             {
                 "name": "intermediates",
                 "secret_ref":"http://<host>:9311/v1/a759452216fd41cf8ee5aba321cfbd49/secrets/8573540e-ad7c-467a-a196-43cf6b5c3468"
             }
         ]

    :return:  URI of the container.

    """

    request = _rest_create_key_container(project_token, region, project_id, container_type, container_name, key_list)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_create_key(project_token, region, project_id, key_name, key, expiration_date, key_type):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    #
    # verify expiration_date
    # If not valid datetime.datetime object set to null so no expiration date
    if not isinstance(expiration_date, datetime.datetime):
        expiration_date = None

    configData = {
        "name": key_name,
        "expiration": str(expiration_date.isoformat()),
        "payload": key,
        "payload_content_type": "text/plain",
        "payload_content_encoding": "base64"
    }

    # verify key_type
    # Valid values: "text/plain", "text/plain;charset=utf-8", "text/plain; charset=utf-8", "application/octet-stream"
    valid_type = ['text/plain', 'text/plain;charset=utf-8', 'text/plain; charset=utf-8', 'application/octet-stream']
    if key_type not in valid_type:
        log.info('_rest_create_key: key_type set to text/plain')
        key_type = valid_type[0]

    # verify key_enconding
    # This item is required if "application/octet-stream" is specified for payload_content_type
    if key_type.count('application/octet-stream'):
        key_encoding = 'base64'
        log.info('_rest_create_key: key_encoding set to base64')
    else:
        log.info('_rest_create_key: key_encoding removed from configData')
        del configData['payload_content_encoding']

    url = 'https://keymanagement.' + region + '.cloud.global.fujitsu.com/v1/' + project_id +'/secrets'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        log.info('_rest_key_create: output')
        log.info(json.dumps(configData, indent=4))
        return request


def create_key(project_token, region, project_id, key_name, key, expiration_date, key_type):
    """
    Create a key.

    :param project_token: A valid K5 project token
    :param region:  A valid K5 region
    :param project_id: K5 Project ID
    :param key_name: Name of the key
    :param key: Content of the key
    :param expiration_date: Python datetime.datetime object with expiration date and time on it.
                            If omitted expiration is disabled. (optional)
    :param key_type: (string) Valid values: 'text/plain', 'text/plain;charset=utf-8',
                     'text/plain; charset=utf-8', 'application/octet-stream'

    :return: URI of the key.
    """
    request = _rest_create_key(project_token, region, project_id, key_name, key, expiration_date, key_type)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()

def _rest_list_keys(project_token, region, project_id):
    headers = {'Content-Type': 'application/json',
              'Accept': 'application/json',
              'X-Auth-Token': project_token}

    url = 'https://keymanagement.' + region + '.cloud.global.fujitsu.com/v1/' + project_id +'/secrets'


    try:
       request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
         # Whoops it wasn't a 200
         log.error(str(e))
         return 'Error: ' + str(e)
    else:
         return request


def list_keys(project_token, region, project_id):
    """
    List key metadata  for project in region.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param project_id: a Valid project id

    :return: JSON that contains key metadata if successful. Otherwise error from requests library.

    """
    request = _rest_list_keys(project_token, region, project_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()

def _rest_list_keys_container(project_token, region, project_id):
    headers = {'Content-Type': 'application/json',
              'Accept': 'application/json',
              'X-Auth-Token': project_token}

    url = 'https://keymanagement.' + region + '.cloud.global.fujitsu.com/v1/' + project_id +'/containers'


    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
         # Whoops it wasn't a 200
         log.error(str(e))
         return 'Error: ' + str(e)
    else:
         return request


def list_keys_container(project_token, region, project_id):
    """
    List key metadata containers.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param project_id: a Valid project id

    :return: JSON that contains key metadata containers if successful. Otherwise error from requests library.

    """
    request = _rest_list_keys_container(project_token, region, project_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()
