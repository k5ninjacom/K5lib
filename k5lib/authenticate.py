import requests
import json
import logging

log = logging.getLogger(__name__)


def _rest_global_authenticate(user, password, contract):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}

    configData = {'auth': {
        'identity': {
            'methods': [
                'password'
            ],
            'password': {
                'user': {
                    'domain': {
                        'name': contract
                    },
                    'name': user,
                    'password': password
                }
            }
        },
    },
    }

    url = 'https://identity.gls.cloud.global.fujitsu.com/v3/auth/tokens'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def get_global_token(user, password, contract):
    """

    Get token to authenticate global services.

    :param user: Valid K5 user.
    :param password: Valid K5 password
    :param contract: K5 domain name.
    :return: Global token if succesfull otherwise error from requests library.

    """
    request = _rest_global_authenticate(user, password, contract)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.headers['X-Subject-Token']


def get_domain_id(user, password, contract):
    """

    Get domain ID.

    :param user: Valid K5 user.
    :param password: Valid K5 password
    :param contract: K5 domain name.
    :return: Domain ID if succesfull otherwise error from requests library.

    """
    request = _rest_global_authenticate(user, password, contract)
    if 'Error' in str(request):
        return str(request)
    else:
        r = request.json()
        return r['token']['user']['domain']['id']


def get_defaultproject_id(user, password, contract):
    """
    Get default project ID.

    :param user: Valid K5 user.
    :param password: Valid K5 password
    :param contract: K5 domain name.
    :return: Domain default project ID if succesfull otherwise error from requests library.

    """
    request = _rest_global_authenticate(user, password, contract)
    if 'Error' in str(request):
        return str(request)
    else:
        r = request.json()
        return r['token']['project']['id']


def _rest_region_authenticate(user, password, contract, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}

    configData = {'auth': {
        'identity': {
            'methods': [
                'password'
            ],
            'password': {
                'user': {
                    'domain': {
                        'name': contract
                    },
                    'name': user,
                    'password': password
                }
            }
        },
    },
    }

    url = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/auth/tokens'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def get_region_token(user, password, contract, region):
    """

    Get token to authenticate on region level services.

    :param user: Valid K5 user.
    :param password: Valid K5 password
    :param contract: K5 domain name.
    :param region: K5 region name.
    :return: Token scoped to region if succesfully. Otherwise error from requests library.

    """
    request = _rest_region_authenticate(user, password, contract, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.headers['X-Subject-Token']


def get_region_info(user, password, contract, region):
    """

    Get region information.

    :param user: Valid K5 user.
    :param password: Valid K5 password
    :param contract: K5 domain name.
    :param region: K5 region name.
    :return: JSON if succesfully. Otherwise error from requests library.

    """
    r = _rest_region_authenticate(user, password, contract, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return r.json()


def _rest_project_authenticate(user, password, contract, project_name, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json'}

    configData = {
        'auth': {
            'identity': {
                'methods': [
                    'password'
                ],
                'password': {
                    'user': {
                        'domain': {
                            'name': contract
                        },
                        'name': user,
                        'password': password
                    }
                }
            },
            'scope': {
                'project': {
                    'name': project_name,
                    'domain': {
                        'name': contract
                    },
                },
            },
        },
    }
#    print(json.dumps(configData, indent=4))

    url = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/auth/tokens'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def get_project_token(user, password, contract, project_name, region):
    """
    Get token to authenticate on project.

    :param user: Valid K5 user.
    :param password: Valid K5 password
    :param contract: K5 domain name.
    :param project_name: K5 project name.
    :param region: K5 region name.
    :return: Token scoped to project if succesfull. Otherwise error from requests library.

    """
    request = _rest_project_authenticate(user, password, contract, project_name, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.headers['X-Subject-Token']


def get_project_id(user, password, contract, project_name, region):
    """
    Get ID for a project.

    :param user: Valid K5 user.
    :param password: Valid K5 password
    :param contract: K5 domain name.
    :param project_name: K5 project name.
    :param region: K5 region name.
    :return: ID if succesfull. Otherwise error from requests library.

    """
    request = _rest_project_authenticate(user, password, contract, project_name, region)
    if 'Error' in str(request):
        return str(request)
    else:
        r = request.json()
        return r['token']['project']['id']


def get_project_info(user, password, contract, project_name, region):
    """

    Get information about a user.

    :param user: Valid K5 user.
    :param password: Valid K5 password
    :param contract: K5 domain name.
    :param project_name: K5 project name.
    :param region: K5 region name.
    :return: JSON if succesfull. Otherwise error from requests library.

    """
    request = _rest_project_authenticate(user, password, contract, project_name, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()
