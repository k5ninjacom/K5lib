from os import environ as env

import requests
import json
import logging

from openstack import connection
from openstack import profile
from openstack import utils
from openstack import identity

utils.enable_logging(debug=True, path='openstack.log')

# links:
# http://developer.openstack.org/api-ref/identity/v3/index.html
# http://stackoverflow.com/questions/33698861/openstack-novaclient-python-api-not-working
# http://developer.openstack.org/sdks/python/openstacksdk/
# http://docs.openstack.org/developer/python-keystoneclient/api/keystoneclient.auth.identity.v3.html#keystoneclient.auth.identity.v3.Password
# http://developer.openstack.org/sdks/python/openstacksdk/users/connection.html


def create_connection(auth_url, region, project_name, project_domain_name, user_domain_name, username, password):
    prof = profile.Profile()
    prof.set_region(profile.Profile.ALL, region)
    prof.set_version('identity', 'v3')

    return connection.Connection(
        profile=prof,
        user_agent='MHApythonDemo',
        auth_plugin='v3password',

        auth_url=auth_url,
        password=password,
        username=username,
        user_domain_name=user_domain_name,
        project_name= project_name,
        project_domain_name= project_domain_name
    )

def authenticate():
    auth_url = env['OS_AUTH_URL']
    region = env['OS_REGION_NAME']
    domain_name = env['OS_USER_DOMAIN_NAME']

    project_domain_name = env['OS_USER_DOMAIN_NAME']
    project_name = env['OS_PROJECT_NAME']

    user_domain_name = env['OS_USER_DOMAIN_NAME']
    username = env['OS_USERNAME']
    password = env['OS_PASSWORD']

    # Create a connection and use authorize method to fetch token
    conn = create_connection(auth_url, region, project_name, project_domain_name, user_domain_name, username, password)

    token = conn.authorize()
    return token

def rest_global_authenticate(user, password, contract):
    """
       https://k5-doc.jp-east-1.paas.cloud.global.fujitsu.com/doc/en/iaas/document/k5-iaas-api-reference_management-administration.pdf
       1.1.5.2  Authenticate (POST /v3/auth/tokens)

       "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "domain": {
                            "name": "domain name"
                        },
                        "name": "username",
                        "password": "userpassword9999"
                    }
                }
            }
       }
    }

    Perform authentication using one of the following combinations:
    • User ID and password
    • Domain ID, user name, and password
    • Domain name, user name, and password (we use this one here)

    HTTP status code
    Returns the HTTP status code of the request.
    One of the following values will be returned:
   201: Normal completion
   400: Invalid access (invalid parameter, etc.)
   401: Authentication error
   403: Cannot access (no privileges)
   404: No applicable resources
   409: Data conflict occurred
   500: Unexpected error
   501: Has not been implemented
   503: Cannot use service
   """
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
        r = requests.post(url, json=configData, headers=headers)
        logging.info(r)

        return r
    except:
        logging.debug(r)
        logging.debug(r.json)
        return


def get_global_token(user, password, contract):

    r = rest_global_authenticate(user, password, contract)

    return r.headers['X-Subject-Token']


def get_domain_id(user, password, contract):

    request = rest_global_authenticate(user, password, contract)
    r = request.json()
    return r['token']['user']['domain']['id']


def get_defaultproject_id(user, password, contract):
    request = rest_global_authenticate(user, password, contract)
    r = request.json()
    return r['token']['project']['id']


def rest_region_authenticate(user, password, contract, region):
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

    url = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/auth/tokens'

    try:
        r = requests.post(url, json=configData, headers=headers)
        logging.info(r)

        return r
    except:
#         logging.debug(r)
#         logging.debug(r.json)
         return


def get_region_token(user, password, contract, region):
    r = rest_region_authenticate(user, password, contract, region)
    return r.headers['X-Subject-Token']


def get_region_info(user, password, contract, region):
    r = rest_region_authenticate(user, password, contract, region)

    return r.json()



def rest_project_authenticate(user, password, contract, projectName, region):
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
            },
        'scope' : {
            'project' : {
                'name' : projectName
            },
        },
        },
    },
    }

    url = 'https://identity.' + region + \
        '.cloud.global.fujitsu.com/v3/auth/tokens'

    try:
        r = requests.post(url, json=configData, headers=headers)
        logging.info(r)

        return r
    except:
#         logging.debug(r)
#         logging.debug(r.json)
         return

def get_project_token(user, password, contract, projectName, region):
    r = rest_project_authenticate(user, password, contract, projectName, region)

    return r.headers['X-Subject-Token']