import requests
import json
import logging

log = logging.getLogger(__name__)


# Rest call to list regions
def rest_list_regions(globalToken):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': globalToken}

    url = 'https://identity.gls.cloud.global.fujitsu.com/v3/regions'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        return 'Error: ' + str(e)
    else:
        return request


# list regions
# returns list of regions
def list_regions(domainToken):

    request = rest_list_regions(domainToken)
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


# Show region
def rest_show_region(domainToken, regionId):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': domainToken}

    url = 'https://identity.gls.cloud.global.fujitsu.com/v3/regions/' + regionId

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


def show_region(domainToken, regionId):
    request = rest_show_region(domainToken, regionId)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


# https:// contract.gls.cloud.global.fujitsu.com
# POST /v1/contracts/{domain_id}?action=startRegion
def rest_activate_region(domainToken, domainId, regionId):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': domainToken}

    configData = {'contract': {
                     'regions': [
                          {
                              'id': regionId
                          }
                     ]
                 }
    }

    url = 'https://contract.gls.cloud.global.fujitsu.com/v1/contracts/' + domainId + '?action=startRegion'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def activate_region(domainToken, domainId, regionId):
    request = rest_activate_region(domainToken, domainId, regionId)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_create_project(regionToken, domainId, region, projectName):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': regionToken}

    configData = {"project": {
                     "description": "Programatically created project",
                     "domain_id": domainId,
                     "enabled": True,
                     "is_domain": False,
                     "name": projectName}
                  }

    url = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/projects?domain_id=' + domainId

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_project(regionToken, domainId, region, projectName):
    request = _rest_create_project(regionToken, domainId, region, projectName)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


# TODO: user details, object or simple list of variables?
def _rest_create_user(globalToken):
    headers = {'Token': globalToken,
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


def create_user(projectToken, region):
    request = _rest_stub(projectToken, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()
