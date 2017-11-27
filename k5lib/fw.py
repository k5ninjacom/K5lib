"""FW module.

FW module provide functions to firewall service of Fujitsu K5 cloud REST API

"""
import requests
import json
import logging
import base64
import uuid


log = logging.getLogger(__name__)


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



def _rest_create_firewall_rule(project_token, region, az, rule_name,  rule_description,  destination_ip,
                               destination_port, protocol,  rule_action,  ):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = { "firewall_rule": {
        "action": rule_action,
        "description": rule_description,
        "destination_ip_address": destination_ip,
        "destination_port": destination_port,
        "enabled": true,
        "ip_version": 4,
        "name": rule_name,
        "protocol": protocol,
        "shared": false,
        "source_ip_address": None,
        "source_port": None,
        "availability_zone": az
     }
    }

    url = 'https://network.' + region + '.cloud.global.fujitsu.com/v2.0/fw/firewall_rules'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_firewall_rule(project_token, region):
    request = _rest_create_firewall_rule(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()