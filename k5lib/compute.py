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