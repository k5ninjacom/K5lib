"""network module
   .. module:: network
"""
import requests
import json
import logging

log = logging.getLogger(__name__)


def _rest_create_network_connector(project_token, project_id, region, connector_name):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {'network_connector': {
        'name': connector_name,
        'tenant_id': project_id}
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


def create_network_connector(project_token, project_id, region, connector_name):
    """create_network_connector.

    :param project_token: A valid K5 project token
    :param project_id:
    :param region:
    :param connector_name:
    :return: Network connector ID or error from requests library

    """
    request = _rest_create_network_connector(project_token, project_id, region, connector_name)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['network_connector']['id']


def _rest_create_network_connector_endpoint(project_token, project_id, region, az, endpointName, networkconnectorId):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"network_connector_endpoint": {
        "name": endpointName,
        "network_connector_id": networkconnectorId,
        "endpoint_type": "availability_zone",
        "location": az,
        "tenant_id": project_id
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


def create_network_connector_endpoint(project_token, project_id, region, az, endpointName, networkconnectorId):
    """create_network_connector_endpoint.

    Create a endpoint into specified network connector

    :param project_token: A valid K5 project token.
    :param project_id: Valid K5 project ID
    :param region: region code eg fi-1
    :param az: az code eg fi1-a
    :param endpointName: Name of endpoint
    :param networkconnectorId: valid ID for network connector
    :return: ID of connector if succesfull. Otherwise error code from requests library.

    """
    request = _rest_create_network_connector_endpoint(project_token, project_id, region, az, endpointName,
                                                      networkconnectorId)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['network_connector_endpoint']['id']


def _rest_create_inter_project_connection(project_token, region, routerId, portId):
    """_rest_create_inter_project_connection.

    https://allthingscloud.eu/2017/01/18/k5-inter-project-routing-fully-automated-shared-services-api-deployment/

    :param project_token: A valid K5 project token
    :param region:
    :param routerId:
    :param portId:
    :return:
    """
    headers = {'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"port_id": portId}

    url = 'https://networking-ex.' + region + '.cloud.global.fujitsu.com/v2.0/routers/' + routerId + '/add_cross_project_router_interface'

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_inter_project_connection(project_token, region, routerId, portId):
    """create_inter_project_connection.

    Add an interface from a subnet in a different project to the router in the project.

    :param project_token: A valid K5 project token.
    :param region: Region of target project
    :param routerId: ID of the router at target project
    :param portId: ID of port at source project
    :return: ID of inter project connection if succesfull. Otherwise error code from requests library.
    """
    request = _rest_create_inter_project_connection(project_token, region, routerId, portId)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['id']


def _rest_delete_inter_project_connection(project_token, region, routerId, portId):
    headers = {'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"port_id": portId}

    url = 'https://networking-ex.' + region + '.cloud.global.fujitsu.com/v2.0/routers/' + routerId + '/remove_cross_project_router_interface'

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def delete_inter_project_connection(project_token, region, routerId, portId):
    """delete_inter_project_connection.

    Delete an interface from a subnet in a different project to the router in the project.

    :param project_token: A valid K5 project token.
    :param region: Region of target project.
    :param routerId: ID of the router at target project.
    :param portId: ID of port at source project.
    :return: ID of inter project connection if succesfull. Otherwise error code from requests library.

    """
    request = _rest_delete_inter_project_connection(project_token, region, routerId, portId)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['id']


def _rest_update_inter_project_connection(project_token, region, routerId, routes):
    headers = {'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"router": {
        "routes": routes}
    }

    url = 'https://networking-ex.' + region + '.cloud.global.fujitsu.com/v2.0/routers/' + routerId

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def update_inter_project_connection(project_token, region, routerId, routes):
    """update_inter_project_connection.

     Update the routing information between different tenants within the same domain.

    :param project_token: A valid K5 project token
    :param region:
    :param routerId:
    :param routes: List of dictionaries in format:
                    {"nexthop":"IPADDRESS",
                     "destination":"CIDR"}
    :return:

    """
    request = _rest_update_inter_project_connection(project_token, region, routerId, routes)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['id']


def _rest_create_port_on_network(project_token, region, az, port_name, securitygroupId, networkId, subnetId=None, ipAddress=None):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    if ipAddress is None:
        configData = {"port": {
            "network_id": networkId,
            "name": port_name,
            "admin_state_up": True,
            "availability_zone": az,
            "security_groups":
                [securitygroupId]}
        }
    else:
        configData = {"port": {
            "network_id": networkId,
            "name": port_name,
            "admin_state_up": True,
            "availability_zone": az,
            "fixed_ips": [{
                "ip_address": ipAddress,
                "subnet_id": subnetId}],
            "security_groups":
                [securitygroupId]}
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


def create_port_on_network(project_token, region, az, port_name, securitygroupId, networkId, subnetId=None,
                           ipAddress=None):
    """create_port_on_network.

    :param project_token: A valid K5 project token
    :param region:
    :param az:
    :param port_name:
    :param securitygroupId:
    :param networkId:
    :param subnetId:
    :param ipAddress:
    :return:   json of succesfull operation. Otherwise error code from requests library.

    """
    request = _rest_create_port_on_network(project_token, region, az, port_name, securitygroupId, networkId, subnetId,
                                           ipAddress)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['port'].get('id')


def _rest_list_ports(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/ports'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def list_ports(project_token, region):
    """list_ports.

    :param project_token:  A valid K5 project token.
    :param region:
    :return: JSON if succesfull. Otherwise error code from requests library.

    """
    request = _rest_list_ports(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def get_port_id(project_token, region, port_name):
    """get_port_id.

    Get ID of the port.

    :param project_token:  A valid K5 project token.
    :param region:
    :param port_name:
    :return: JSON if succesfull. Otherwise error code from requests library.

    """
    request = _rest_list_ports(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()

        # Get ID of our connector from info
        outputList = []
        outputDict = request['ports']

        counter = 0
        for i in outputDict:
            if str(i['name']) == port_name:
                outputList.append(str(i['id']))
                counter += 1

        return outputList[0]


def _rest_delete_port(project_token, region, portId):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/ports/' + portId

    try:
        request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def delete_port(project_token, region, portId):
    """delete_port.

    :param project_token: A valid K5 project token
    :param region:
    :param portId:
    :return:

    """
    request = _rest_delete_port(project_token, region, portId)
    if 'Error' in str(request):
        return str(request)
    else:
        return request


def _rest_list_network_connectors(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connectors'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def list_network_connectors(project_token, region):
    """list_network_connectors.

    :param project_token: A valid K5 project token
    :param region:
    :return: JSON that contains network connectors if succesfull. Otherwise error from requests library.

    """
    request = _rest_list_network_connectors(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def get_network_connector_id(project_token, region, connector_name):
    """get_network_connector_id.

    :param project_token: A valid K5 project token.
    :param region:
    :param connector_name:
    :return: ID of the connector if succesfull. Otherwise error from requests library

    """
    request = _rest_list_network_connectors(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()

        # Get ID of our connector from info
        outputList = []
        outputDict = request['network_connectors']

        counter = 0
        for i in outputDict:
            if str(i['name']) == connector_name:
                outputList.append(str(i['id']))
                counter += 1

        return outputList[0]


def _rest_delete_network_connector(project_token, region, networkConnectorId):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connectors' + '/' + networkConnectorId

    try:
        request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def delete_network_connector(project_token, region, networkConnectorId):
    """delete_network_connector.

    :param project_token:  A valid K5 project token.
    :param region:
    :param networkConnectorId:
    :return:
    """
    request = _rest_list_network_connectors(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def _rest_list_network_connector_endpoints(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def list_network_connector_endpoints(project_token, region):
    """list_network_connector_endpoints.

    List network connector endpoints.

    :param project_token:  A valid K5 project token.
    :param region:
    :return:

    """
    request = _rest_list_network_connector_endpoints(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def get_network_connector_endpoint_id(project_token, region, endpointName):
    """get_network_connector_endpoint_id.

    Get an ID for network connector endpoint.

    :param project_token: A valid K5 project token.
    :param region:
    :param endpointName:
    :return: ID if succesfull. Otherwise error from requests library.

    """
    request = _rest_list_network_connector_endpoints(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        # Get ID of our connector endpoint from info
        outputList = []
        outputDict = request['network_connector_endpoints']

        counter = 0
        for i in outputDict:
            if str(i['name']) == endpointName:
                outputList.append(str(i['id']))
                counter += 1

        return outputList[0]


def _rest_connect_network_connector_endpoint(project_token, region, endpointId, portId):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"interface": {
        "port_id": portId}
    }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints/' + endpointId + '/connect'

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def connect_network_connector_endpoint(project_token, region, endpointId, portId):
    """connect_network_connector_endpoint.

    :param project_token: A valid K5 project token
    :param region:
    :param endpointId:
    :param portId:
    :return: JSON if succesfull operation. Otherwise error code from requests library.

    """
    request = _rest_connect_network_connector_endpoint(project_token, region, endpointId, portId)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def _rest_disconnect_network_connector_endpoint(project_token, region, endpointId, portId):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"interface": {
        "port_id": portId}
    }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints/' + endpointId + '/disconnect'

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def disconnect_network_connector_endpoint(project_token, region, endpointId, portId):
    """disconnect_network_connector_endpoint.

    :param project_token: A valid K5 project token
    :param region:
    :param endpointId:
    :param portId:
    :return: JSON if succesfull operation. Otherwise error code from requests library.

    """
    request = _rest_disconnect_network_connector_endpoint(project_token, region, endpointId, portId)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def _rest_delete_network_connector_endpoint(project_token, region, connectorEndpointId):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints' + '/' + connectorEndpointId

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def delete_network_connector_endpoint(project_token, region, connectorEndpointId):
    """delete_network_connector_endpoint.

    Delete network connector endpoint.

    :param project_token: A valid K5 project token
    :param region:
    :param connectorEndpointId:
    :return: JSON if succesfull operation. Otherwise error code from requests library.

    """
    request = _rest_delete_network_connector_endpoint(project_token, region, connectorEndpointId)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def _rest_create_network(project_token, region, az, networkName):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"network": {
                  "name": networkName,
                  "admin_state_up": True,
                  "availability_zone": az}
                  }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/networks'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_network(project_token, region, az, networkName):
    """create_network.

    Create a network into project.

    :param project_token: A valid K5 project token.
    :param region: Region
    :param az: AZ for example fi-1a
    :param networkName: Name of the network.
    :return: ID of network if suucesfull, otherwise error from requests lib

    """
    request = _rest_create_network(project_token, region, az, networkName)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['network']['id']


def _rest_create_subnet(project_token, region,  network_id, cidr, subnet_name, version, az,
                        allocation_pools, dns_nameservers, host_routes, gateway_ip):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"subnet": {
                  "name": subnet_name,
                  "network_id": network_id,
                  "ip_version": version,
                  "cidr": cidr,
                  "availability_zone": az,
                  "allocation_pools": allocation_pools,
                  "dns_nameservers": dns_nameservers,
                  "host_routes": host_routes,
                  "gateway_ip": gateway_ip}
                  }

    # Remove optional variables that are empty. This prevents 400 errors from api.
    for key in list(configData['subnet']):
        if configData['subnet'][key] is None:
            del configData['subnet'][key]

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/subnets'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_subnet(project_token, region, network_id, cidr, subnet_name='subnet', version='4', az=None,
                  allocation_pools=None, dns_nameservers=None, host_routes=None, gateway_ip=None):
    """create_subnet.

    Create a subnet.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param network_id: ID for network
    :param cidr: (string). For example:'192.168.199.0/24'
    :param subnet_name: (optional) Name of the subnet, eg 'subnet'
    :param version: IP version '4' or '6'
    :param az: AZ name eg f1-1a
    :param allocation_pools: (optional) (Dict)
                             The start and end addresses for the allocation pools.
    :param dns_nameservers: (optional)
                            A list of DNS name servers for the subnet.
                            For example ["8.8.8.7", "8.8.8.8"].
                            The specified IP addresses are displayed in sorted order in ascending order.
                            The lowest IP address will be the primary DNS address.
    :param host_routes: (optional)
                        A list of host route dictionaries for the subnet. For example:
                        "host_routes":[
                             {
                             "destination":"0.0.0.0/0",
                             "nexthop":"172.16.1.254"
                              },
                             {
                             "destination":"192.168.0.0/24",
                             "nexthop":"192.168.0.1"
                             }
                        ]
    :param gateway_ip: (optional)
    :return: Subnet ID if succesfull, otherwise error from request library

    """
    request = _rest_create_subnet(project_token, region,  network_id, cidr, subnet_name, version, az,
                                  allocation_pools, dns_nameservers, host_routes, gateway_ip)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['subnet']['id']
