"""
network module.

 Functions related networks, routers, network connectors, vpn  etc are here.

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
    """
    Create a network connector.

    :param project_token: A valid K5 project token
    :param project_id: K5 project ID
    :param region: K5 region name.
    :param connector_name: Connector name.
    :return: Network connector ID or error from requests library

    """
    request = _rest_create_network_connector(project_token, project_id, region, connector_name)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['network_connector']['id']


def _rest_create_network_connector_endpoint(project_token, project_id, region, az, endpoint_name, networkconnector_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"network_connector_endpoint": {
        "name": endpoint_name,
        "network_connector_id": networkconnector_id,
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


def create_network_connector_endpoint(project_token, project_id, region, az, endpoint_name, networkconnector_id):
    """

    Create a endpoint into specified network connector.

    :param project_token: A valid K5 project token.
    :param project_id: Valid K5 project ID
    :param region: K5 region name.
    :param az: K5 availability zone name.
    :param endpoint_name: Name of endpoint
    :param networkconnector_id: network connector ID
    :return: ID of connector if succesfull. Otherwise error code from requests library.

    """
    request = _rest_create_network_connector_endpoint(project_token, project_id, region, az, endpoint_name,
                                                      networkconnector_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['network_connector_endpoint']['id']


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
    """

    List network connector endpoints.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :return: JSON if succesfull. Otherwise error code from requests library.

    """
    request = _rest_list_network_connector_endpoints(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def get_network_connector_endpoint_id(project_token, region, endpoint_name):
    """

    Get an ID for network connector endpoint.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :param endpoint_name: Endpoint name.
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
            if str(i['name']) == endpoint_name:
                outputList.append(str(i['id']))
                counter += 1

        return outputList[0]


def _rest_get_network_connector_endpoint_info(project_token, region, network_connector_endpoint_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints/' + network_connector_endpoint_id

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def get_network_connector_endpoint_info(project_token, region, network_connector_endpoint_id):
    """

    List network connector endpoints.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :param network_connector_endpoint_id: ID of network connection
    :return: JSON if succesfull. Otherwise error code from requests library.

    """
    request = _rest_get_network_connector_endpoint_info(project_token, region, network_connector_endpoint_id)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def _rest_list_network_connector_endpoint_interfaces(project_token, region, network_connector_endpoint_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints/' \
          + network_connector_endpoint_id + '/interfaces'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def list_network_connector_endpoint_interfaces(project_token, region, network_connector_endpoint_id):
    """

    List network connector endpoint interfaces.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :param network_connector_endpoint_id: ID of network connection
    :return: JSON if succesfull. Otherwise error code from requests library.

    """
    request = _rest_list_network_connector_endpoint_interfaces(project_token, region, network_connector_endpoint_id)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def _rest_create_inter_project_connection(project_token, region, router_id, port_id):
    headers = {'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"port_id": port_id}

    url = 'https://networking-ex.' + region + '.cloud.global.fujitsu.com/v2.0/routers/' + router_id + '/add_cross_project_router_interface'

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def create_inter_project_connection(project_token, region, router_id, port_id):
    """

    Add an interface from a subnet in a different project to the router in the project.

    :param project_token: A valid K5 project token.
    :param region: Region of target project
    :param router_id: ID of the router at target project
    :param port_id: ID of port at source project
    :return: ID of inter project connection if succesfull. Otherwise error code from requests library.

    """
    request = _rest_create_inter_project_connection(project_token, region, router_id, port_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['id']


def _rest_delete_inter_project_connection(project_token, region, router_id, port_id):
    headers = {'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"port_id": port_id}

    url = 'https://networking-ex.' + region + '.cloud.global.fujitsu.com/v2.0/routers/' + router_id + '/remove_cross_project_router_interface'

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def delete_inter_project_connection(project_token, region, router_id, port_id):
    """

    Delete an interface from a subnet in a different project to the router in the project.

    :param project_token: A valid K5 project token.
    :param region: Region of target project.
    :param router_id: ID of the router at target project.
    :param port_id: ID of port at source project.
    :return: ID of inter project connection if succesfull. Otherwise error code from requests library.

    """
    request = _rest_delete_inter_project_connection(project_token, region, router_id, port_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['id']


def _rest_update_inter_project_connection(project_token, region, router_id, routes):
    headers = {'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"router": {
        "routes": routes}
    }

    url = 'https://networking-ex.' + region + '.cloud.global.fujitsu.com/v2.0/routers/' + router_id

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def update_inter_project_connection(project_token, region, router_id, routes):
    """

     Update the routing information between different tenants within the same domain.

    :param project_token: A valid K5 project token
    :param region: K5 region name
    :param router_id: Router ID.
    :param routes: List of dictionaries in format:
                    {"nexthop":"IPADDRESS",
                     "destination":"CIDR"}
    :return: ID of connection if succesfull. Otherwise error from requests library.

    """
    request = _rest_update_inter_project_connection(project_token, region, router_id, routes)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['id']


def _rest_create_port_on_network(project_token, region, az, port_name, securitygroup_id, network_id, subnet_id=None, ip_address=None):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    if ip_address is None:
        configData = {"port": {
            "network_id": network_id,
            "name": port_name,
            "admin_state_up": True,
            "availability_zone": az,
            "security_groups":
                [securitygroup_id]}
        }
    else:
        configData = {"port": {
            "network_id": network_id,
            "name": port_name,
            "admin_state_up": True,
            "availability_zone": az,
            "fixed_ips": [{
                "ip_address": ip_address,
                "subnet_id": subnet_id}],
            "security_groups":
                [securitygroup_id]}
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


def create_port_on_network(project_token, region, az, port_name, securitygroup_id, network_id, subnet_id=None,
                           ip_address=None):
    """
    Create a port on network.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param az: K5 availability zone name.
    :param port_name: Port name.
    :param securitygroup_id: Security group ID.
    :param network_id: Network ID.
    :param subnet_id: Subnet ID.
    :param ip_address: IP address for the port.
    :return: JSON if succesfull. Otherwise error code from requests library.

    """
    request = _rest_create_port_on_network(project_token, region, az, port_name, securitygroup_id, network_id, subnet_id,
                                           ip_address)
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
    """
    List ports.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :return: JSON if succesfull. Otherwise error code from requests library.

    """
    request = _rest_list_ports(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def get_port_id(project_token, region, port_name):
    """

    Get ID of the port.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :param port_name: Port name.
    :return: ID if succesfull. Otherwise error code from requests library.

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


def _rest_delete_port(project_token, region, port_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/ports/' + port_id

    try:
        request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def delete_port(project_token, region, port_id):
    """

    Delete port.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param port_id: Port ID.
    :return: Http 204 if succesfull. Otherwise error code from requests library.

    """
    request = _rest_delete_port(project_token, region, port_id)
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
    """
    List network connectors visible for project in region.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :return: JSON that contains network connectors if succesfull. Otherwise error from requests library.

    """
    request = _rest_list_network_connectors(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def get_network_connector_id(project_token, region, connector_name):
    """
    Get ID of network connector.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :param connector_name: Connector name.
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


def _rest_delete_network_connector(project_token, region, networkConnector_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connectors' + '/' + networkConnector_id

    try:
        request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def delete_network_connector(project_token, region, networkConnector_id):
    """
    Delete network connector.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :param networkConnector_id: Network connector ID
    :return:  Http 204 if succesfull. Otherwise error code from requests library.

    """
    request = _rest_delete_network_connector(project_token, region, networkConnector_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request


def _rest_connect_network_connector_endpoint(project_token, region, endpoint_id, port_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"interface": {
        "port_id": port_id}
    }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints/' + endpoint_id + '/connect'

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def connect_network_connector_endpoint(project_token, region, endpoint_id, port_id):
    """
    Connect networkc connector with endpoint.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param endpoint_id: Endpoint ID.
    :param port_id: Port ID.
    :return: JSON if succesfull operation. Otherwise error code from requests library.

    """
    request = _rest_connect_network_connector_endpoint(project_token, region, endpoint_id, port_id)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def _rest_disconnect_network_connector_endpoint(project_token, region, endpoint_id, port_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"interface": {
        "port_id": port_id}
    }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints/' + endpoint_id + '/disconnect'

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def disconnect_network_connector_endpoint(project_token, region, endpoint_id, port_id):
    """

    Disconnect networkc connector from endpoint.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param endpoint_id: Endpoint ID.
    :param port_id: Port ID.
    :return: JSON if succesfull operation. Otherwise error code from requests library.

    """
    request = _rest_disconnect_network_connector_endpoint(project_token, region, endpoint_id, port_id)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def _rest_delete_network_connector_endpoint(project_token, region, connector_endpoint_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connector_endpoints' + '/' + connector_endpoint_id

    try:
        request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def delete_network_connector_endpoint(project_token, region, connector_endpoint_id):
    """

    Delete network connector endpoint.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param connector_endpoint_id: Network connecto ID.
    :return: Http result code 204 succesfull operation. Otherwise error code from requests library.

    """
    request = _rest_delete_network_connector_endpoint(project_token, region, connector_endpoint_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request


def _rest_create_network(project_token, region, az, network_name):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"network": {
                  "name": network_name,
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


def create_network(project_token, region, az, network_name):
    """

    Create a network into project.

    :param project_token: A valid K5 project token.
    :param region: Region
    :param az: AZ for example fi-1a
    :param network_name: Name of the network.
    :return: ID of network if suucesfull, otherwise error from requests lib

    """
    request = _rest_create_network(project_token, region, az, network_name)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['network']['id']


def _rest_list_networks(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/networks'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def _rest_delete_network(project_token, region, network_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/networks/' + network_id

    try:
        request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def delete_network(project_token, region, network_id):
    """
    Delete subnet.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param network_id: ID for network to delete.
    :return: Http returncode 204 if succesful. otherwise error code from requests library.

    """
    request = _rest_delete_network(project_token, region, network_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request


def list_networks(project_token, region):
    """
    List networks visible for project in region.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :return: JSON that contains networks if succesfull. Otherwise error from requests library.

    """
    request = _rest_list_networks(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def get_network_id(project_token, region, network_name):
    """
    Get ID of network.

    :param project_token: A valid K5 project token.
    :param region: K5 region name.
    :param network_name: Network name.
    :return: ID of the connector if succesfull. Otherwise error from requests library

    """
    request = _rest_list_networks(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()

        # Get ID of our connector from info
        outputList = []
        outputDict = request['networks']

        counter = 0
        for i in outputDict:
            if str(i['name']) == network_name:
                outputList.append(str(i['id']))
                counter += 1

        return outputList[0]


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
    """

    Create a subnet.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param network_id: ID for network
    :param cidr: (string). For example:'192.168.199.0/24'
    :param subnet_name: (optional) Name of the subnet, eg 'subnet'
    :param version: IP version '4' or '6'
    :param az: AZ name eg f1-1a
    :param allocation_pools: (optional) (Dict) The start and end addresses for the allocation pools.
    :param dns_nameservers: (optional) A list of DNS name servers for the subnet.
                            For example: ["8.8.8.7", "8.8.8.8"].
                            The specified IP addresses are displayed in sorted order in ascending order.
                            The lowest IP address will be the primary DNS address.
    :param host_routes: (optional) A list of host route dictionaries for the subnet. For example:
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


def _rest_delete_subnet(project_token, region, subnet_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/subnets/' + subnet_id

    try:
        request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def delete_subnet(project_token, region, subnet_id):
    """
    Delete subnet.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param subnet_id: ID for subnet to delete.
    :return: Http returncode 204 if succesful. otherwise error code from requests library.

    """
    request = _rest_delete_subnet(project_token, region, subnet_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request


def _rest_list_subnets(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/subnets'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        return request


def list_subnets(project_token, region):
    """
    List subnets visible for project in region.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :return: JSON that contains subnets if succesfull. Otherwise error from requests library.

    """
    request = _rest_list_subnets(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_create_security_group(project_token, region, name, description):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {'security_group': {
                     'name': name,
                     'description': description
                      }
                  }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/security-groups'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_security_group(project_token, region, name, description):
    """
    Create a security group.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param name: Name of security group
    :param description: Description for security group.
    :return: Security group ID if succesfull, otherwise error from request library.

    """
    request = _rest_create_security_group(project_token, region, name, description)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['security_group']['id']


def _rest_list_security_groups(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}


    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/security-groups'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def list_security_groups(project_token, region):
    """
    List security groups visible to project

    :param project_token:
    :param region:

    :return: JSON if succesfull, otherwise error from request library.
    """

    request = _rest_list_security_groups(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def get_security_group_id(project_token, region, sg_name):
    """
    Get ID of the security group.

    :param project_token:
    :param region:
    :param sg_name:
    :return: ID of security group if succesfull. Otherwise error code from requests library.

    """
    request = _rest_list_security_groups(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()

        # Get ID of our connector from info
        outputList = []
        outputDict = request['security_groups']

        counter = 0
        for i in outputDict:
            if str(i['name']) == sg_name:
                outputList.append(str(i['id']))
                counter += 1

        return outputList[0]


def _rest_create_security_group_rule(project_token, region, security_group_id, direction, ethertype, protocol, port_range_min, port_range_max, remote_ip_prefix, remote_group_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {'security_group_rule': {
                     'direction': direction,
                     'port_range_min': port_range_min,
                     'ethertype': ethertype,
                     'port_range_max': port_range_max,
                     'protocol': protocol,
                     'remote_group_id': remote_group_id,
                     'security_group_id': security_group_id,
                     'remote_ip_prefix': remote_ip_prefix
    }
    }

    # Remove optional variables that are empty. This prevents 400 errors from api.
    for key in list(configData['security_group_rule']):
        if configData['security_group_rule'][key] is None:
            del configData['security_group_rule'][key]

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/security-group-rules'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request



def create_security_group_rule(project_token, region, security_group_id, direction, ethertype='IPv4', protocol=None,
                               port_range_min=None, port_range_max=None, remote_ip_prefix=None, remote_group_id=None):
    """
    Create security group rule.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param security_group_id: ID of the security group.
    :param direction: Ingress or egress: The direction in which the security group rule is applied.
                      For a compute instance, an ingress security group rule is applied to incoming (ingress)
                      traffic for that instance. An egress rule is applied to traffic leaving the instance.
    :param ethertype: Must be IPv4, and addresses represented in CIDR must match the ingress or egress rules. If this
                      values is not specified, IPv4 is set.
    :param protocol: The protocol that is matched by the security group rule. Valid values are null, tcp, udp, icmp,
                     and digits between 0-and 255.
    :param port_range_min: The minimum port number in the range that is matched by the security group rule.
                           When the protocol is TCP or UDP, this value must be less than or equal to the value of
                           the port_range_max attribute. If this value is not specified, the security group rule
                           matches all numbers of port. If port_range_min is 0, all port numbers are allowed regardless
                           of port_range_max.
                           When the protocol is ICMP, this value must be an ICMP type. If this value is not specified,
                           the security group rule matches all ICMP types.
    :param port_range_max: The maximum port number in the range that is matched by the security group rule.
                           When the protocol is TCP or UDP , the port_range_min attribute constrains the port_range_max
                           attribute.
                           When the protocol is ICMP, this value must be an ICMP code. If this value is not specified,
                           the security group rule matches all ICMP codes.
    :param remote_ip_prefix: The remote IP prefix to be associated with this security group rule. You can specify
                             either remote_group_id or remote_ip_prefix in the request body. This attribute matches the
                             specified IP prefix as the source or destination IP address of the IP packet.
                             If direction is ingress matches source, otherwise matches destination.
    :param remote_group_id: The remote group ID to be associated with this security group rule. You can specify either
                            remote_group_id or remote_ip_prefix.
    :return: Security group ID if succesfull, otherwise error from request library.

    """
    request = _rest_create_security_group_rule(project_token, region, security_group_id, direction, ethertype, protocol,
                                               port_range_min, port_range_max,  remote_ip_prefix, remote_group_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['security_group_rule']['id']


def _rest_create_router(project_token, region, name, az, admin_state_up):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {'router': {
                     'name': name,
                     'availability_zone': az,
                     'admin_state_up': admin_state_up
                      }
                  }

    # Remove optional variables that are empty. This prevents 400 errors from api.
    for key in list(configData['router']):
        if configData['router'][key] is None:
            del configData['router'][key]

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/routers'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_router(project_token, region, name=None, az=None, admin_state_up=None):
    """
    Create router.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param name: Name of the router.
    :param az: AZ name eg f1-1a.
    :param admin_state_up: The administrative state of the
                           router, which is up (true) or down (false).
    :return: Router ID if succesfull, otherwise error from request library.

    """
    request = _rest_create_router(project_token, region, name, az, admin_state_up)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['router']['id']


def _rest_update_router(project_token, region, router_id, name, az, admin_state_up, network_id, route_table):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {'router': {
                     'name': name,
                     'availability_zone': az,
                     'admin_state_up': admin_state_up,
                     'external_gateway_info': {
                         'network_id': network_id
                      },
                     'routes': {
                         route_table,
                      }
                      }
                  }
    # Remove optional variables that are empty. This prevents 400 errors from api.
    for key in list(configData['router']):
        if configData['router'][key] is None:
            del configData['router'][key]
    if configData['router']['external_gateway_info']['network_id']is None:
        del configData['router']['external_gateway_info']['network_id']
        del configData['router']['external_gateway_info']
    if configData['router']['routes'] is None:
        del configData['router']['routes']

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/routers/' + router_id

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def update_router(project_token, region, router_id, name=None, az=None, admin_state_up=None, network_id=None, route_table=None):
    """
    Update router.

    :param project_token: Valid K5 project token
    :param region: K5 Region eg 'fi-1'
    :param router_id: ID of the router
    :param name: Name of the router.
    :param az: AZ name eg f1-1a.
    :param admin_state_up: The administrative state of the
                           router, which is up (true) or down (false).
    :param network_id: ID of external network.
    :param route_table: [
           {
            "nexthop":"10.1.0.10",
            "destination":"40.0.1.0/24"
           }
           ]
    :return: JSON if succesfull otherwise error from reguests library.

    """
    request = _rest_update_router(project_token, region, router_id, name, az, admin_state_up, network_id, route_table)

    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()
