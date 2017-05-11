import requests
import json
import logging

log = logging.getLogger(__name__)


def _rest_get_vnc_console_url(projectToken, projectId, region, serverId):
    """get_vnc_console_url.

    Get url for vm console access.

    :param projectToken:
    :param projectId:
    :param region:
    :param serverId:
    :return: json of succesfull operation. Otherwise error code from requests library.
    """
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': projectToken}

    configData = {'os-getVNCConsole': {
        'type': 'novnc'
        }
    }

    url = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + projectId + '/servers/' + serverId + '/action'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def get_vnc_console_url(projectToken, projectId, region, serverId):
    """

    :param projectToken:
    :param projectId:
    :param region:
    :param serverId:
    :return:
    """
    request = _rest_get_vnc_console_url(projectToken, projectId, region, serverId)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_create_keypair(projectToken, projectId, region, az, keypairName='default'):
    """_rest_showkeypair.

    Internal rest call to show keypair information.

    :param projectToken: Valid K5 project scope token.
    :param projectId: valid id for project
    :param region: region code eg fi-1
    :param az: az code eg fi-1a
    :param keypairName: name of the keypair to be created.
    :return: json of succesfull operation. Otherwise error code from requests library.

    """
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': projectToken}

    configData = {"keypair": {
                      "name": keypairName,
                      "availability_zone": az
                       }
    }

    url = 'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + projectId + '/os-keypairs'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_keypair(projectToken, projectId, region, az, keypairName):
    """create_keypair.

    Create a new keypair.

    Args:
        projectToken (token): Valid K5 project scope token.
        projectId: valid id for project
        region (string): region code eg fi-1
        az (string): az code eg fi-1a
        keypairName (string) name of the keypair to be created.

    Returns:
        json of succesfull operation. Otherwise error code from requests library.

    """
    request = _rest_create_keypair(projectToken, projectId, region, az, keypairName)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


