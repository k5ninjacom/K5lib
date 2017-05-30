"""
Orchestration module.

 orchestration module provide functions to orchestration service of Fujitsu K5 cloud REST API

"""
import requests
import json
import logging

log = logging.getLogger(__name__)


def _rest_create_stack(project_token, region, project_id, stack_name, template):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"stack_name": stack_name,
                  "template": template,
                  "disable_rollback": True,
                  "timeout_mins": 60
                  }
    # from portal https://orchestration.fi-1.cloud.global.fujitsu.com/v1/e77679bd08104b0483d5cd5aba0f704d
    # from log:   https://orchestration.fi-1.cloud.global.fujitsu.com/v1/9c15ef58ce7e42098e1844b5d81202fe/stacks
    url = 'https://orchestration.' + region + '.cloud.global.fujitsu.com/v1/' + project_id + '/stacks'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_stack(project_token, region, project_id, stack_name, template):
    """
    Create a new stack into project.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param project_id: ID of the project
    :param stack_name: The name of a stack to be created.
                  Specify a string of halfwidth
                  alphanumeric characters, underscores
                  (_), hyphens (-), and periods (.), and
                  that starts with a letter. The maximum
                  length is 255 characters. Subsequent
                  characters are ignored.
    :param template: A valid JSON.
    :return: JSON if succesfull. Otherwise error code from requests library.

    """
    request = _rest_create_stack(project_token, region, project_id, stack_name, template)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_delete_stack(project_token, region, project_id, stack_name, stack_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://orchestration.' + region + '.cloud.global.fujitsu.com/v1/' + project_id + '/stacks' + '/' + stack_name + '/' + stack_id

    try:
        request = requests.delete(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def delete_stack(project_token, region, project_id, stack_name, stack_id):
    """
    Delete_stack.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param project_id: ID of the project
    :param stack_name: Name of the stack
    :param stack_id: ID of the stack
    :return: JSON if succesfull. Otherwise error code from requests library.

    """
    request = _rest_delete_stack(project_token, region, project_id, stack_name, stack_id)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def _rest_get_stack_info(project_token, project_id, region, stack_name, stack_id):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': project_token
               }

    url = 'https://orchestration.' + region + '.cloud.global.fujitsu.com/v1/' + project_id + '/stacks/' + stack_name + '/' + stack_id

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('headers:')
        log.error(headers)
        log.error('url')
        log.error(url)
        return 'Error: ' + str(e)
    else:
        return request


def get_stack_info(project_token, project_id, region, stack_name, stack_id):
    """
    Get detailed  stack info.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param project_id: ID of the project
    :param stack_name: Name of the stack
    :param stack_id: ID of the stack
    :return: JSON if succesfull. Otherwise error code from requests library.

    """
    request = _rest_get_stack_info(project_token, project_id, region, stack_name, stack_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_list_stacks(project_token, region, project_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://orchestration.' + region + '.cloud.global.fujitsu.com/v1/' + project_id + '/stacks'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def list_stacks(project_token, region, project_id):
    """
    List stacks in project.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param project_id: ID of the project
    :return: JSON if succesfull. Otherwise error code from requests library.

    """
    request = _rest_list_stacks(project_token, region, project_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def get_stack_id(project_token, region, project_id, stack_name):
    """
    Get stack ID.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param project_id: ID of the project
    :param stack_name: Name of the stack
    :return: Stack ID if succesfull. Otherwise error code from requests library.

    """
    request = _rest_list_stacks(project_token, region, project_id)

    if 'Error' in str(request):
        return str(request)
    else:
        outputDict = request["stacks"]
        counter = 0
        for i in outputDict:
            if stack_name in str(i['name']):
                returnValue = (str(i['id']))
                counter += 1
        return returnValue
