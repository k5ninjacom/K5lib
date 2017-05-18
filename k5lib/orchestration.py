"""orchestration module.

orchestration module provide functions to orchestration service of Fujitsu K5 cloud REST API

"""
import requests
import json
import logging

log = logging.getLogger(__name__)


def _rest_create_stack(projectToken, region, projectId, stackName, template):
    """_rest_create_stack.

    Param:
       stackName: The name of a stack to be created.
                  Specify a string of halfwidth
                  alphanumeric characters, underscores
                  (_), hyphens (-), and periods (.), and
                  that starts with a letter. The maximum
                  length is 255 characters. Subsequent
                  characters are ignored.
       template:  The string for a template. Use escape
                  characters in the template if necessary
                  so that the correct JSON format is used in
                  the request body. For example, replace
                  double quotation marks (") with (\"), and
                  line feeds with (\n).
    Returns:
        TYPE: Description

    """
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': projectToken}

    configData = {"stack_name": stackName,
                  "template": template,
                  "disable_rollback": True,
                  "timeout_mins": 60
                  }
# from portal https://orchestration.fi-1.cloud.global.fujitsu.com/v1/e77679bd08104b0483d5cd5aba0f704d
# from log:   https://orchestration.fi-1.cloud.global.fujitsu.com/v1/9c15ef58ce7e42098e1844b5d81202fe/stacks
    url = 'https://orchestration.' + region + '.cloud.global.fujitsu.com/v1/' + projectId + '/stacks'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_stack(projectToken, region, projectId, stackName, template):
    """create_stack.

    :param projectToken:
    :param region:
    :param projectId:
    :param stackName:
    :param template:
    :return:

    """
    request = _rest_create_stack(projectToken, region, projectId, stackName, template)
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
    """delete_stack.

    :param project_token:
    :param region:
    :param project_id:
    :param stack_name:
    :param stack_id:
    :return:

    """
    request = _rest_delete_stack(project_token, region, project_id, stack_name, stack_id)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()
        return request


def _rest_get_stack_info(projectToken, projectId, region, stackName, stackId):
    """_rest_get_stack_info.

    :param projectToken:
    :param projectId:
    :param region:
    :param stackName:
    :param stackId:
    :return:

    GET /v1/{tenant_id}/stacks/{stack_name}/{stack_id}

    """
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': projectToken
               }

    url = 'https://orchestration.' + region + '.cloud.global.fujitsu.com/v1/' + projectId + '/stacks/' + stackName + '/' + stackId

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


def get_stack_info(projectToken, projectId, region, stackName, stackId):
    """get_stack_info.

    :param projectToken:
    :param projectId:
    :param region:
    :param stackName:
    :param stackId:
    :return: JSON if succesfull otherwise error code from requests library.

    """
    request = _rest_get_stack_info(projectToken, projectId, region, stackName, stackId)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_list_stacks(project_token, region, project_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://orchestration.' + region + '.cloud.global.fujitsu.com/v1/' + project_id + '/stacks/'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def list_stacks(project_token, region, project_id):
    request = _rest_list_stacks(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def get_stack_id(project_token, region, project_id, stack_name):
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
