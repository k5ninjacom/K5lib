import requests
import json
import logging

log = logging.getLogger(__name__)

def _rest_create_stack(projectToken, region, projectId, stackName, template):
    """Summary
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
               'Accept' : 'application/json',
               'X-Auth-Token': projectToken}

    configData = { "stack_name": stackName,
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
    request = _rest_create_stack(projectToken, region, projectId, stackName, template)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()
