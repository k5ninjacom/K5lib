"""
Compute module.

 Compute module provide functions to compute service of Fujitsu K5 cloud REST API

"""
import requests
import json
import logging
import base64

log = logging.getLogger(__name__)


def _rest_get_vnc_console_url(project_token, project_id, region, server_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {'os-getVNCConsole': {
        'type': 'novnc'
        }
    }

    url = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + project_id + '/servers/' + server_id + '/action'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def get_vnc_console_url(project_token, project_id, region, server_id):
    """
    Get a url to connect VNC into vm console.

    :param project_token: Valid K5 project token.
    :param project_id: K5 project ID
    :param region: K5 region name
    :param server_id: server ID
    :return: JSON if succesfull. Otherwise error from requests library.

    """
    request = _rest_get_vnc_console_url(project_token, project_id, region, server_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_create_keypair(project_token, project_id, region, az, keypair_name='default'):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"keypair": {
                  "name": keypair_name,
                  "availability_zone": az}
                  }

    url = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + project_id + '/os-keypairs'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_keypair(project_token, project_id, region, az, keypair_name):
    """
    Create a keypair to logging in vm.

    :param project_token: Valid K5 project token.
    :param project_id: K5 project ID.
    :param region: K5 region name.
    :param az: K5 availability zone name.
    :param keypair_name: Name of keypair.
    :return: JSON if succesfull. Otherwise error from requests library.

    """
    request = _rest_create_keypair(project_token, project_id, region, az, keypair_name)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request

def _rest_get_server_password(project_token, region, project_id, server_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}


    url = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + project_id + '/servers/' + server_id + '/os-server-password'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(headers)
        log.error(url)
        log.error(request.json())
        log.error(str(e))
        return 'Error: ' + str(e)
    else:
        log.info(request)
        log.info(headers)
        log.info(url)
        log.info(request.json())
        return request


def get_server_password(project_token, region, project_id, server_id):
    """
    Get server password hash. You need to decrypt hash with private key to get password.

    :param project_token: Valid K5 project token.
    :param region: K5 region name.
    :param project_id: K5 project ID
    :param server_id: ID of the server

    :return: Password hash as a binary object if succesfull. Otherwise error from requests library.
    """
    request = _rest_get_server_password(project_token, region, project_id, server_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return base64.b64decode(request.json()['password'])


def _rest_list_servers(project_token, region, project_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + project_id + '/servers'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        return 'Error: ' + str(e)
    else:
        return request


def list_servers(project_token, region, project_id):
    """
    Get list of servers in project.

    :param project_token: Valid K5 project token.
    :param region: K5 region name.
    :param project_id: K5 project ID
    :return: JSON with list of servers if succesfull. Otherwise error from requests library.
    """

    request = _rest_list_servers(project_token, region, project_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def get_server_id(project_token, region, project_id, server_name):
    """
    Get ID of the server. Returns first server found that match server_name parameter.

    :param project_token: Valid K5 project token.
    :param region: K5 region name.
    :param project_id: K5 project ID
    :param server_name: Name of the server
    :return: ID of the server if succesfull. Otherwise error from requests library.
    """

    request = _rest_list_servers(project_token, region, project_id)

    if 'Error' in str(request):
        log.error(str(request))
        return str(request)
    else:
        # loop trough servers and return first that match

        outputList = []
        outputDict = request['servers']

        for i in outputDict:
            if server_name in str(i['name']):
                outputList.append(str(i['id']))

        return outputList[0]


def get_server_name(project_token, region, project_id, server_id):
    """
    Get name of the server. Returns first server found that match server_id parameter.

    :param project_token: Valid K5 project token.
    :param region: K5 region name.
    :param project_id: K5 project ID
    :param server_id: ID of the server
    :return: Name of the server if succesfull. Otherwise error from requests library.
    """

    request = _rest_list_servers(project_token, region, project_id)

    if 'Error' in str(request):
        log.error(str(request))
        return str(request)
    else:
        # loop trough servers and return first that match

        outputList = []
        outputDict = request['servers']

        for i in outputDict:
            if server_id in str(i['id']):
                outputList.append(str(i['name']))

        return outputList[0]


def _rest_get_server_info(project_token, region, project_id, server_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}


    url = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + project_id + '/servers/' + server_id

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        return 'Error: ' + str(e)
    else:
        return request


def get_server_info(project_token, region, project_id, server_id):
    """
    Get detailed information about server.

    :param project_token: Valid K5 project token.
    :param region: K5 region name.
    :param project_id: K5 project ID
    :param server_id: ID of the server

    :return: JSON if succesfull. Otherwise error from requests library.
    """

    request = _rest_get_server_info(project_token, region, project_id, server_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_add_server_interface(project_token, region, project_id, server_id, net_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"interfaceAttachment":{
        "net_id": net_id
        }
    }

    url = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + \
           project_id + '/servers/' + server_id + '/os-interface'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def add_server_interface(project_token, region, project_id, server_id, net_id):
    """ Add interface into server.

    :param project_token: Valid K5 project token.
    :param region: K5 region name.
    :param project_id: K5 project ID
    :param server_id: ID of the server
    :param net_id: ID of the network interface is connected
    :return: JSON if succesful. otherwise error from request library.

    """
    request = _rest_add_server_interface(project_token, region, project_id, server_id, net_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_list_server_interfaces(project_token, region, project_id, server_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + \
           project_id + '/servers/' + server_id + '/os-interface'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        return 'Error: ' + str(e)
    else:
        return request


def list_server_interfaces(project_token, region, project_id, server_id):
    """ List interfaces from server.

    :param project_token: Valid K5 project token.
    :param region: K5 region name.
    :param project_id: K5 project ID
    :param server_id: ID of the server

    :return: JSON containing list of interfaces if succesful. otherwise error from request library.
    """
    request = _rest_list_server_interfaces(project_token, region, project_id, server_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_get_server_interface_info(project_token, region, project_id, server_id, port_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + \
           project_id + '/servers/' + server_id + '/os-interface/' +  port_id

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        return 'Error: ' + str(e)
    else:
        return request


def get_server_interface_info(project_token, region, project_id, server_id, port_id):
    """

    :param project_token: Valid K5 project token.
    :param region: K5 region name.
    :param project_id: K5 project ID
    :param server_id: ID of the server
    :param port_id: ID of port (interface) we are intrested.

    :return:  JSON containing info of interface if succesful. otherwise error from request library.
    """
    request = _rest_get_server_interface_info(project_token, region, project_id, server_id, port_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_detach_server_interface(project_token, region, project_id, server_id, port_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + \
           project_id + '/servers/' + server_id + '/os-interface/' +  port_id

    try:
        request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        return 'Error: ' + str(e)
    else:
        return request


def detach_server_interface(project_token, region, project_id, server_id, port_id):
    """ Detach interface from server.

    :param project_token: Valid K5 project token.
    :param region: K5 region name.
    :param project_id: K5 project ID
    :param server_id: ID of the server
    :param port_id: ID of port (interface) we are deleting.

    :return:  http 202 response if succesful. Otherwise error from request library.

    """
    request = _rest_detach_server_interface(project_token, region, project_id, server_id, port_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()

""" 
Todo: finalize this after get flawor ID and list flawors  

def _rest_create_server(project_token, region, project_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"server": {
            "name": name,
            "availability_zone": az,
            "imageRef": "",
            "flavorRef": flavor_id,
            "key_name": keyname,
            "block_device_mapping_v2": [{
                "boot_index": "0",
                "uuid": windows_image_ref_id,
                "volume_size": vol_size,
                "device_name": device_name,
                "source_type": source,
                "destination_type": destination,
                "delete_on_termination": isdelete }],
            "max_count": instance_max,
            "min_count": instance_min,
            "networks": [{"uuid": network_id}],
            "security_groups": [{"name": sg_name}],
            "os:scheduler_hints": {"fcx.dedicated": "true"}
    }
    }


    url = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + project_id + '/servers/'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_server(project_token, region):
    request = _rest_create_server(project_token, region, project_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()
"""


def _rest_list_flavors(project_token, region, project_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + project_id + '/flavors'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        return 'Error: ' + str(e)
    else:
        return request


def list_flavors(project_token, region, project_id):
    """ List available flavors

    :param project_token: Valid K5 project token.
    :param region: K5 region name.
    :param project_id: K5 project ID

    :return: JSON containing list of available flavors if succesful, otherwise error from requests library.
    """
    request = _rest_list_flavors(project_token, region, project_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def get_flavor_id(project_token, region, project_id, flavor_name):
    """ Get ID for flavor name

    :param project_token: Valid K5 project token.
    :param region: K5 region name.
    :param project_id: K5 project ID.
    :param flavor_name: Name of the flavor.

    :return: ID of flavor if succesful, otherwise error from requests library.
    """
    request = _rest_list_flavors(project_token, region, project_id)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()

        # Get ID of our connector from info
        outputList = []
        outputDict = request['flavors']

        counter = 0
        for i in outputDict:
            if str(i['name']) == flavor_name_name:
                outputList.append(str(i['id']))
                counter += 1
        if counter > 0:
            return outputList[0]
        else:
            return 'Error: Not found'



