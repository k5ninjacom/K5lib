import requests
import json
import logging

log = logging.getLogger(__name__)


def _rest_get_vnc_console_url(projectToken, projectId, region, serverId):
    """

    :param projectToken:
    :param projectId:
    :param region:
    :param serverId:
    :return:
    """
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': projectToken}

    configData = {'os-getVNCConsole': {
        'type': 'novnc'
        }
    }

    # from log:   https://compute.uk-1.cloud.global.fujitsu.com/v2/9c15ef58ce7e42098e1844b5d81202fe
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
    request = _rest_get_vnc_console_url(projectToken, projectId, region, serverId)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_create_keypair(projectToken, projectId, region, az, keypairName='default'):
    """_rest_showkeypair.

    Internal rest call to show keypair information.

    Args:
        projectToken (token): Valid K5 project scope token.
        region: (string): region code eg fi-1

    Returns:
        json of succesfull operation. Otherwise error code from requests library.

    """
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': projectToken}

    configData = {"keypair": {
                      "name": keypairName,
                      "availability_zone": az
                       }
    }

    'https://compute.' + region + '.cloud.global.fujitsu.com/v2/' + projectId + '/os-keypairs'

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
        projectId (id):
        region: (string): region code eg fi-1

    Returns:
        json of succesfull operation. Otherwise error code from requests library.

    """
    request = _rest_create_keypair(projectToken, projectId, region, az, keypairName)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


