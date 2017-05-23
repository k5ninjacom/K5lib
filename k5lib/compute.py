"""
Compute module.

 Compute module provide functions to compute service of Fujitsu K5 cloud REST API

"""
import requests
import json
import logging

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
