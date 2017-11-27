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
                               destination_port, protocol, source_ip, source_port,  rule_action, enabled):

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = { "firewall_rule": {
        "action": rule_action,
        "description": rule_description,
        "destination_ip_address": destination_ip,
        "destination_port": destination_port,
        "enabled": enabled,
        "ip_version": 4,
        "name": rule_name,
        "protocol": protocol,
        "source_ip_address": source_ip,
        "source_port": source_port,
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


def create_firewall_rule(project_token, region, az, rule_name,  rule_description,  destination_ip,
                         destination_port, protocol, source_ip, source_port, rule_action, enabled=True):
    """
    Create firewall rule.

    :param project_token: A Valid K5 project token
    :param region: A valid K5 region
    :param az: A valid K5 availability zone
    :param rule_name: (string) Name of the firewall rule
    :param rule_description: (string) Description of the rule
    :param destination_ip: (string) IP or CIDR of  destination address.
    :param destination_port: (string) Destination port number or a range. If range, port numbers are separated by colon.
                             Specify a small port number first.
    :param protocol: (string) The protocol that is matched by the firewall rule. Valid values are null, tcp, udp, and icmp.
                              (Avoid the use of null when specifying the protocol for Neutron FWaaS rules. Instead,
                              create multiple rules for both 'tcp' and 'udp' protocols independently.)
    :param source_ip:  (string) IP or CIDR of source address.
    :param source_port: (string) Destination port number or a range. If range, port numbers are separated by colon.
                                 Specify a small port number first.
    :param rule_action: (string) Action to be performed on the traffic matching the rule (allow, deny).
    :param enabled: (bool) When set to False will disable this rule in the firewall policy.
                           Facilitates selectively turning off rules without having to disassociate the rule from the firewall policy.
    :return: JSON if succesful. Otherwise error from requests library.
    """
    request = _rest_create_firewall_rule(project_token, region, az, rule_name,  rule_description,  destination_ip,
                                         destination_port, protocol, source_ip, source_port,  rule_action, enabled)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_create_firewall_policy(project_token, region, az, policy_name, policy_description, firewall_rules):

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"firewall_policy": {
        "firewall_rules": firewall_rules,
        "name": policy_name,
        "description": policy_description,
        "availability_zone": az
     }
    }

    url = 'https://network.' + region + '.cloud.global.fujitsu.com/v2.0/fw/firewall_policies'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_firewall_policy(project_token, region, az, policy_name, policy_description, firewall_rules):
    """
    Creates firewall policy.

    :param project_token: A valid K5 token.
    :param region: A valid K5 region.
    :param az: A valid K5 az.
    :param policy_name: (string) Name of the policy.
    :param policy_description: (string) Description of the policy.
    :param firewall_rules: (list) List of firewall rule ID:s

    :return: JSON if succesfull. Otherwise error from requests library.
    """

    request = _rest_create_firewall_policy(project_token, region, az, policy_name, policy_description, firewall_rules)

    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_create_firewall(project_token, region, az, router_id, firewall_policy_id, firewall_name, firewall_description,
                          admin_state):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"firewall": {
        "name": firewall_name,
        "description": firewall_description,
        "admin_state_up": admin_state,
        "firewall_policy_id": firewall_policy_id,
        "router_id": router_id,
        "availability_zone": az
    }
}

    url = 'https://network.' + region + '.cloud.global.fujitsu.com/v2.0/fw/firewalls'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_firewall(project_token, region, az, router_id, firewall_policy_id, firewall_name='FW_',
                    firewall_description = 'default_FW', admin_state=True):
    """
    Creates a firewall.

    :param project_token: A valid K5 project token
    :param region:  A valid K5 region.
    :param az: A valid K5 availability zone.
    :param router_id: ID of the router where firewall is configured.
    :param firewall_policy_id: ID of the policy to be used for firewall configuration.
    :param firewall_name: (optional) Name of the firewall.
    :param firewall_description: (optional) Description of firewall.
    :param admin_state: (bool) Administrative state of the firewall. If false (down), firewall does not forward packets
                               and will drop all traffic to/from VMs behind the firewall.

    :return: JSON if succesfull. Otherwise error from requests library.
    """

    request = _rest_create_firewall(project_token, region, az, router_id, firewall_policy_id, firewall_name,
                                    firewall_description, admin_state)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()

