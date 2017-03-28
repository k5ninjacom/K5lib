import requests
import json
import logging


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