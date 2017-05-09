import requests
import json
import logging

log = logging.getLogger(__name__)




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
    request =  _rest_create_network_connector(projectToken, projectid, connectorName, region)
    if 'Error' in str(request):
        return str(request)
    else:
        r = request.json()
        return r


def _rest_create_network_connector_endpoint(projectToken, projectId, region, az, endpointName, networkconnectorId):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': projectToken}

    configData = {"network_connector_endpoint": {
                      "name": endpointName,
                      "network_connector_id": networkconnectorId,
                      "endpoint_type": "availability_zone",
                      "location": az,
                      "tenant_id": projectId
                 }
    }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_network_connector_endpoint(projectToken, projectId, region, az, endpointName, networkconnectorId):
    """create_network_connector_endpoint.

    Create a endpoint into specified network connector

    Args:
        projectToken (token): Valid K5 project scope token.
        projectId (id): Valid K5 project ID
        region: (string): region code eg fi-1
        az (string): az code eg fi1-a
        endpointName (string): Name of endpoint
        networkconnectorId (id): valid ID for network connector

    Returns:
        json of succesfull operation. Otherwise error code from requests library.

    """
    request = _rest_create_network_connector_endpoint(projectToken, projectId, region, az, endpointName, networkconnectorId)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def create_inter_project_connection(projectToken, region):
    request = _rest_stub(projectToken, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def create_inter_az_onnection(projectToken, region):
    request = _rest_stub(projectToken, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


