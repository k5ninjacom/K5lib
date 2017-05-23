"""
contract module.

 Functions related contract, regions, user account, projects etc are here.

"""

import requests
import json
import logging

log = logging.getLogger(__name__)


def _rest_list_regions(global_token):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': global_token}

    url = 'https://identity.gls.cloud.global.fujitsu.com/v3/regions'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        return 'Error: ' + str(e)
    else:
        return request


def list_regions(domain_token):
    """
    List K5 regions.

    :param domain_token: Valid K5 domain token.
    :return: JSON if succesfull. Otherwise error from requests library.

    """
    request = _rest_list_regions(domain_token)
    if 'Error' in str(request):
        return str(request)
    else:
        r = request.json()
        regionsList = []
        regionsDict = r['regions']

        counter = 0
        for i in regionsDict:
            if str(i['parent_region_id']) == 'None':
                regionsList.append(str(i['id']))
                counter += 1

        return regionsList


def _rest_show_region(domain_token, region_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': domain_token}

    url = 'https://identity.gls.cloud.global.fujitsu.com/v3/regions/' + region_id

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('headers:')
        log.error(headers)
        log.error('url:')
        log.error(url)
        return 'Error: ' + str(e)
    else:
        return request


def show_region(domain_token, region_id):
    """
    Show detailed region info.

    :param domain_token: Valid K5 region token.
    :param region_id: ID of the region.
    :return: JSON if succesfull. Otherwise error from requests library.

    """
    request = _rest_show_region(domain_token, region_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_activate_region(domain_token, domain_id, region_id):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': domain_token}

    configData = {'contract': {
                     'regions': [
                          {
                              'id': region_id
                          }
                     ]
                 }
    }

    url = 'https://contract.gls.cloud.global.fujitsu.com/v1/contracts/' + domain_id + '?action=startRegion'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def activate_region(domain_token, domain_id, region_id):
    """

    Activate region for the domain.

    :param domain_token: Valid K5 region token.
    :param domain_id: ID of the domain.
    :param region_id: ID of the region.
    :return: JSON if succesfull. Otherwise error from requests library.

    """
    request = _rest_activate_region(domain_token, domain_id, region_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_create_project(region_token, domain_id, region, project_name):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': region_token}

    configData = {"project": {
                     "description": "Programatically created project",
                     "domain_id": domain_id,
                     "enabled": True,
                     "is_domain": False,
                     "name": project_name}
                  }

    url = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/projects?domain_id=' + domain_id

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_project(region_token, domain_id, region, project_name):
    """
    Create a new project into domain.

    :param region_token: Valid K5 region token.
    :param domain_id: ID of the domain.
    :param region: K5 region name
    :param project_name: Project name.
    :return: JSON if succesfull. Otherwise error from requests library.

    """
    request = _rest_create_project(region_token, domain_id, region, project_name)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


# TODO: user details, object or simple list of variables?
def _rest_create_user(global_token):
    headers = {'Token': global_token,
               'Content-Type': 'application/json'}

    configData = {"user_last_name": userDetails[1],
                  "user_first_name": userDetails[0],
                  "login_id": userDetails[2],
                  "user_description": "Automated Account Setup",
                  "mailaddress": userDetails[3],
                  "user_status": "1",
                  "password": userDetails[4],
                  "language_code": "en",
                  "role_code": "01"
                  }

    url = 'https://k5-apiportal.paas.cloud.global.fujitsu.com/API/v1/api/users'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_user(project_token, region):
    """
    Create new user.

    At the moment this is a placeholder, actual implementation is WIP.

    :param project_token:
    :param region:
    :return:
    """
    request = _rest_stub(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()
