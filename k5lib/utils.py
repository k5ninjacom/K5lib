"""utils.py.

Utility functions for k5lib other modules.

"""
import string
import random
import os
import logging
from collections import abc


def gen_passwd(length=16):
    """gen_passwd.

    Utility function to create a string.
    https://docs.python.org/3/library/secrets.html
    create a alphanumeric password with at least one lowercase character,
    at least one uppercase character, and at least three digits


    Args:
        lenght (int): lenght of returned string. MIN = 5

    Returns:
        String.

    """
    alphabet = string.ascii_letters + string.digits
    # We need to have minimum 5 characters
    if length < 5:
        length == 5
    while True:
        password = ''.join(random.choice(alphabet) for i in range(length))
        if (any(c.islower() for c in password)
            and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password


def create_logfile(logName='default.log', logDir='log'):
    """create_logfile.

    Utility function to create a log file

    Args:
        logname (string): name of log file.
        logDir: (string): Working folder for log file

    Returns:
        none.

    """
    if not os.path.exists(logDir):
        os.makedirs(logDir)
    logging.basicConfig(filename=logDir + '/' + logName, level=logging.DEBUG)
    logging.info('Logging started')
    return


def recursive_items(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield (key, value)
            yield from recursive_items(value)
        else:
            yield (key, value)


def replace_none_values(dictionary):
    for key, value in dictionary.items():
        if type(value) is dict:
            yield (key, value)
            yield from replace_none_values(value)
        else:
            if value is None:
                dictionary[key] = ''
            yield (key, value)


def _rest_stub(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {'key1': {
                     'key2': [
                          {
                              'key3': 'value3'
                          }
                     ]
                 }
    }

    url = url = 'https://foobar.' + region + '.cloud.global.fujitsu.com/v2.0/ports'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def stub(project_token, region):
    request = _rest_stub(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()
