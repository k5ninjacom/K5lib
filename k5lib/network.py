import requests
import json
import logging

log = logging.getLogger(__name__)


def _rest_create_network_connector(projectToken, projectid, connectorName, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': projectToken}

    configData = {'network_connector': {
                  'name': connectorName,
                  'tenant_id': projectid}
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
    request = _rest_create_network_connector(projectToken, projectid, connectorName, region)
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

    :param projectToken: Valid K5 project scope token.
    :param projectId: Valid K5 project ID
    :param region: region code eg fi-1
    :param az: az code eg fi1-a
    :param endpointName: Name of endpoint
    :param networkconnectorId: valid ID for network connector
    :return: json of succesfull operation. Otherwise error code from requests library.

    """
    request = _rest_create_network_connector_endpoint(projectToken, projectId, region, az, endpointName, networkconnectorId)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def create_inter_project_connection(projectToken, region):
    # TODO:
    # 1. create a network connector
    # 2. create a endpoint1 (az1)
    # 3. create a endpoint2 (az2)
    request = _rest_stub(projectToken, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def create_inter_az_connection(projectToken, projectId, region, az1, az2, endpointName=ep,):
    # TODO:
    # 1. create a network connector
    # 2. create a endpoint1 (az1)
    # 3. create a endpoint2 (az2)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def _rest_create_port_on_network(projectToken, region, az, securitygrouId, ipAddress=None, subnetId=None):
    """_rest_create_port_on_network.

    :param projectToken:  Valid K5 project scope token.
    :param region:  region code eg fi-1
    :param az:
    :param securitygrouId: securitygrouId (optional)
    :param ipAddress: ip adress for port (optional)
    :param subnetId: Valid ID for subnet
    :return: json of succesfull operation. Otherwise error code from requests library.

    """
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': projectToken}

    if ipAddress is None:
        configData = {"port": {
                      "network_id": networkId,
                      "name": portName,
                      "admin_state_up": True,
                      "availability_zone": az,
                      "security_groups":
                      [securitygrouId]}
                      }
    else:
        configData = {"port": {
                      "network_id": networkId,
                      "name": portName,
                      "admin_state_up": True,
                      "availability_zone": az,
                      "fixed_ips": [{
                          "ip_address": ipAddress,
                          "subnet_id": subnetId}],
                      "security_groups":
                      [securitygrouId]}
                      }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/ports'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_port_on_network(projectToken, region, az, securitygrouId, ipAddress=None, subnetId=None):
    """create_port_on_network.

    :param projectToken:
    :param region:
    :param az:
    :param securitygrouId:
    :param ipAddress: (optional)
    :param subnetId: (optional)
    :return:  json of succesfull operation. Otherwise error code from requests library.

    """
    request = create_port_on_network(projectToken, region, az, securitygrouId, ipAddress, subnetId)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def _rest_list_network_connectors(projectToken, region):
    """_rest_stub.

    Example internal rest call.

    Args:
        projectToken (token): Valid K5 project scope token.
        region: (string): region code eg fi-1

    Returns:
        json of succesfull operation. Otherwise error code from requests library.

    """
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': projectToken}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connectors'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def list_network_connectors(projectToken, region):
    """stub.

    Example call that use internal rest call to do actual job.

    Args:
        projectToken (token): Valid K5 project scope token.
        region: (string): region code eg fi-1

    Returns:
        json of succesfull operation. Otherwise error code from requests library.

    """
    request = _rest_list_network_connectors(projectToken, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request
