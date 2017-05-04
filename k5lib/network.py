import requests
import json
import logging

log = logging.getLogger(__name__)


def _rest_stub(projectToken, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': projectToken}

    configData = {'key1': {
                     'key2': [
                          {
                              'key3': 'value3'
                          }
                     ]
                 }
    }

    url = url = 'https://foobar.' + region + '.cloud.global.fujitsu.com/v2.0/ports'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def stub(projectToken, region):
    request = _rest_stub(projectToken, region)
    if 'Error' in str(request):
        return str(request)
    else:
        r = request.json()
        return r


def _rest_create_network_connector(projectToken, projectid, connectorName, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': projectToken}

    configData = {"network_connector": {
                     "name": connectorName,
                     "tenant_id": projectid}
    }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connectors'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_network_connector(projectToken, projectid, connectorName, region):
    request =     k5lib._rest_create_network_connector(projectToken, projectid, connectorName, region)
    if 'Error' in str(request):
        return str(request)
    else:
        r = request.json()
        return r
