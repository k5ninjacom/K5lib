def _rest_list_firewall_rules(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://network.' + region + '.cloud.global.fujitsu.com/v2.0/fw/firewall_rules'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        return 'Error: ' + str(e)
    else:
        return request


def list_firewall_rules(project_token, region):
    """
    List firewall rules visible for the project.

    :param project_token: A valid K5 project token
    :param region: A valid K5 region

    :return: JSON if succesfull, otherwise error from requests library.
    """
    request = _rest_list_firewall_rules(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()