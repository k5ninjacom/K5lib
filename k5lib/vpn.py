"""vpn module.

VPN module provide functions for VPN service of Fujitsu K5 cloud REST API

"""
import requests
import json
import logging as log


def _rest_create_ipsec_vpn_service(project_token, region, az, name, router_id, subnet_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"vpnservice": {
                      "subnet_id": subnet_id,
                      "router_id": router_id,
                      "name": name,
                      "admin_state_up": True,
                      "availability_zone": az
                  }
                  }
    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/vpnservices'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_ipsec_vpn_service(project_token, region, az, name, router_id, subnet_id):
    """
    Create a IPsec vpn service.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param az: Availability zone name.
    :param name: Name for IPsec vpn service.
    :param router_id: ID of router to connect service
    :param subnet_id: ID of subnet to connect service
    :return: ID of IPsec vpn service if succesfull. Otherwise error from requests library.
    """
    request = _rest_create_ipsec_vpn_service(project_token, region, az, name, router_id, subnet_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['vpnservice']['id']


def _rest_list_ipsec_services(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/vpnservices'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def list_ipsec_vpn_services(project_token, region):
    """
    List IPsec VPN services.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :return: JSON that contains IPsec VPN services if succesfull. Otherwise error from requests library.

    """
    request = _rest_list_ipsec_services(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def get_ipsec_vpn_service_id(project_token, region, service_name):
    """
    List IPsec VPN services.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :return: JSON that contains IPsec VPN services if succesfull. Otherwise error from requests library.

    """
    request = _rest_list_ipsec_services(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()

        # Get ID of our connector from info
        outputList = []
        outputDict = request['vpnservices']

        counter = 0
        for i in outputDict:
            if str(i['name']) == service_name:
                outputList.append(str(i['id']))
                counter += 1

        return outputList[0]


def _rest_get_delete_ipsec_vpn_service(http_method, project_token, region, service_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/vpnservices/' + service_id

    try:
        if 'get' in http_method:
            request = requests.get(url, headers=headers)
        else:
            request = requests.delete(url, headers=headers)

        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def get_ipsec_vpn_service_info(project_token, region, service_id):
    """
    Get IPsec VPN service detailed info.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param service_id: ID of the service.
    :return: JSON that contains IPsec VPN service info if succesfull. Otherwise error from requests library.

    """
    http_method = 'get'
    request = _rest_get_delete_ipsec_vpn_service(http_method, project_token, region, service_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def delete_ipsec_vpn_service(project_token, region, service_id):
    """
    Get IPsec VPN service detailed info.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :return: Http 204 code if succesfull. Otherwise error from requests library.

    """
    http_method = 'delete'
    request = _rest_get_delete_ipsec_vpn_service(http_method, project_token, region, service_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return str(request)


def _rest_update_ipsec_vpn_service(project_token, region, az, service_id, name, router_id, subnet_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"vpnservice": {
                      "subnet_id": subnet_id,
                      "router_id": router_id,
                      "name": name,
                      "admin_state_up": True,
                      "availability_zone": az
                  }
                  }
    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/vpnservices/' + service_id

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def update_ipsec_vpn_service(project_token, region, az, service_id, name=None, router_id=None, subnet_id=None):
    """
    Update a IPsec VPN service.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param az: Availability zone name.
    :param name: Name for IPsec VPN service.
    :param service_id: Id of the IPsec VPN service to be updated.
    :param router_id: ID of router to connect service
    :param subnet_id: ID of subnet to connect service
    :return: JSON IPsec vpn service if succesfull. Otherwise error from requests library.

    """
    request = _rest_update_ipsec_vpn_service(project_token, region, az, service_id, name, router_id, subnet_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


########################################################################################################################
# IPsec policy
########################################################################################################################

def _rest_list_ipsec_policies(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/ipsecpolicies'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def list_ipsec_policies(project_token, region):
    """
    List IPsec vpn policies.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :return: JSON that contains ipsec policies if succesfull. Otherwise error from requests library.

    """
    request = _rest_list_ipsec_policies(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def get_ipsec_policy_id(project_token, region, policy_name):
    """
    Get  IPsec VPN policy ID.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param policy_name: IPsec vpn policy name.
    :return: ID of the ipsec policy if succesfull. Otherwise error from requests library.

    """
    request = _rest_list_ipsec_policies(project_token, region)

    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()

        # Get ID of our connector from info
        outputList = []
        outputDict = request['ipsecpolicies']

        counter = 0
        for i in outputDict:
            if str(i['name']) == policy_name:
                outputList.append(str(i['id']))
                counter += 1

        return outputList[0]


def _rest_get_delete_ipsec_policy(http_method, project_token, region, policy_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/ipsecpolicies/' + policy_id

    try:
        if 'get' in http_method:
            request = requests.get(url, headers=headers)
        else:
            request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def get_ipsec_policy_info(project_token, region, policy_id):
    """
    Get detailed info from IPsec vpn policy.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param policy_id: ID of IPsec vpn policy.
    :return: JSON that contains ipsec policies if succesfull. Otherwise error from requests library.

    """
    http_method = 'get'
    request = _rest_get_delete_ipsec_policy(http_method, project_token, region, policy_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def delete_ipsec_policy(project_token, region, policy_id):
    """
    Delete IPsec vpn policy.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param policy_id: ID of IPsec vpn policy to be deleted.
    :return: Http code 204 if succesfull. Otherwise error from requests library.

    """
    http_method = 'delete'
    request = _rest_get_delete_ipsec_policy(http_method, project_token, region, policy_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return str(request)


def _rest_create_update_ipsec_policy(http_method, project_token, region, az, policy_name, transform_protocol,
                                     auth_algorithm, encapsulation_mode, encryption_algorithm, pfs, lifetime):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"ipsecpolicy": {
                      "name": policy_name,
                      "transform_protocol": transform_protocol,
                      "auth_algorithm": auth_algorithm,
                      "encapsulation_mode": encapsulation_mode,
                      "encryption_algorithm": encryption_algorithm,
                      "pfs": pfs,
                      "lifetime": {
                           "units": "seconds",
                           "value": lifetime
                       },
                      "availability_zone": az
                  }
                  }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/ipsecpolicies'

    try:
        if 'post' in http_method:
            request = requests.post(url, json=configData, headers=headers)
        else:
            request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_ipsec_policy(project_token, region, az, policy_name, transform_protocol, auth_algorithm, encapsulation_mode,
                        encryption_algorithm, pfs, lifetime):
    """
    Create a IPsec vpn policy.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param az: Availability zone name.
    :param policy_name: Name of IPsec policy to be created.
    :param transform_protocol:
    :param auth_algorithm:
    :param encryption_algorithm:
    :param pfs:
    :param lifetime:
    :return:

    """
    http_method = 'post'
    request = _rest_create_update_ipsec_policy(http_method, project_token, region, az, policy_name, transform_protocol,
                                               auth_algorithm, encapsulation_mode, encryption_algorithm, pfs, lifetime)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['ipsecpolicy']['id']


def update_ipsec_policy(project_token, region, az, policy_name, transform_protocol, auth_algorithm, encapsulation_mode,
                        encryption_algorithm, pfs, lifetime):
    """
    Update a IPsec vpn policy.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param az: Availability zone name.
    :param policy_name: Name of IPsec policy to be created.
    :param transform_protocol:
    :param auth_algorithm:
    :param encapsulation_mode:
    :param encryption_algorithm:
    :param pfs:
    :param lifetime:
    :return:
    """
    """
    Update a IPsec vpn policy.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param az: Availability zone name.
    :param policy_name: Name of IPsec policy to be created.
    :param transform_protocol:
    :param auth_algorithm:
    :param encryption_algorithm:
    :param pfs:
    :param lifetime:
    :return: JSON of udated ipsec policy if succesfull. Otherwise error from rewuests library.

    """
    http_method = 'put'
    request = _rest_create_update_ipsec_policy(http_method, project_token, region, az, policy_name, transform_protocol,
                                               auth_algorithm, encapsulation_mode, encryption_algorithm, pfs, lifetime)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


########################################################################################################################
# IKE policy
########################################################################################################################
def _rest_list_ike_policies(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/ikepolicies'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def list_ike_policies(project_token, region):
    """
    List IKE vpn policies.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :return: JSON that contains IKE policies if succesfull. Otherwise error from requests library.

    """
    request = _rest_list_ike_policies(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def get_ike_policy_id(project_token, region, policy_name):
    """
    Get  IKE VPN policy ID.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param policy_name: IKE vpn policy name.
    :return: ID of the ike policy if succesfull. Otherwise error from requests library.

    """
    request = _rest_list_ike_policies(project_token, region)

    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()

        # Get ID of our connector from info
        outputList = []
        outputDict = request['ikepolicies']

        counter = 0
        for i in outputDict:
            if str(i['name']) == policy_name:
                outputList.append(str(i['id']))
                counter += 1

        return outputList[0]


def _rest_get_delete_ike_policy(http_method, project_token, region, policy_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/ikepolicies/' + policy_id

    try:
        if 'get' in http_method:
            request = requests.get(url, headers=headers)
        else:
            request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def get_ike_policy_info(project_token, region, policy_id):
    """
    Get detailed info from IKE vpn policy.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param policy_id: ID of IKE vpn policy.
    :return: JSON that contains ike policy information if succesfull. Otherwise error from requests library.

    """
    http_method = 'get'
    request = _rest_get_delete_ike_policy(http_method, project_token, region, policy_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def delete_ike_policy(project_token, region, policy_id):
    """
    Delete IKE vpn policy.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param policy_id: ID of IKE vpn policy to be deleted.
    :return: Http code 204 if succesfull. Otherwise error from requests library.

    """
    http_method = 'delete'
    request = _rest_get_delete_ike_policy(http_method, project_token, region, policy_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return str(request)


def _rest_create_update_ike_policy(http_method, project_token, region, az, policy_name, phase1_negotiation_mode, auth_algorithm, encryption_algorithm, pfs, lifetime, ike_version):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"ikepolicy": {
                     "phase1_negotiation_mode": phase1_negotiation_mode,
                     "auth_algorithm": auth_algorithm,
                     "encryption_algorithm": encryption_algorithm,
                     "pfs": pfs,
                     "lifetime": {
                         "units": "seconds",
                         "value": lifetime
                      },
                     "ike_version": ike_version,
                     "name": policy_name,
                     "availability_zone": az
                  }
                  }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/ikepolicies'

    try:
        if 'post' in http_method:
            request = requests.post(url, json=configData, headers=headers)
        else:
            request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_ike_policy(project_token, region, az, policy_name, phase1_negotiation_mode, auth_algorithm, encryption_algorithm, pfs, lifetime, ike_version):
    """
    Create a IKE vpn policy.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param az: Availability zone name.
    :param policy_name: Name of IKE policy to be created.

    :param project_token:
    :param region:
    :param az:
    :param policy_name:
    :param phase1_negotiation_mode:
    :param auth_algorithm:
    :param encryption_algorithm:
    :param pfs:
    :param lifetime:
    :param ike_version:
    :return: ID of IKE policy if succesfull. Otherwise error from requests library.

    """
    http_method = 'post'
    request = _rest_create_update_ike_policy(http_method, project_token, region, az, policy_name, phase1_negotiation_mode, auth_algorithm, encryption_algorithm, pfs, lifetime, ike_version)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['ikepolicy']['id']


def update_ike_policy(project_token, region, az, policy_name, phase1_negotiation_mode, auth_algorithm, encryption_algorithm, pfs, lifetime, ike_version):
    """
    Update a IKE vpn policy.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param az: Availability zone name.
    :param policy_name: Name of IKE policy to be created.
    :param phase1_negotiation_mode:
    :param auth_algorithm:
    :param encryption_algorithm:
    :param pfs:
    :param lifetime:
    :param ike_version:
    :return: JSON of updated IKE policy if succesfull. Otherwise error from requests library.

    """
    http_method = 'put'
    request = _rest_create_update_ike_policy(http_method, project_token, region, az, policy_name, phase1_negotiation_mode, auth_algorithm, encryption_algorithm, pfs, lifetime, ike_version)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


########################################################################################################################
# IPsec VPN connection
########################################################################################################################
def _rest_create_ipsec_vpn_connection(project_token, region, az, connection_name, ipsecpolicy_id, ikepolicy_id,
                                      vpnservice_id, peer_cidrs, peer_address, psk):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"ipsec_site_connection": {
                     "psk": psk,
                     "initiator": "bi-directional",
                     "ipsecpolicy_id": ipsecpolicy_id,
                     "admin_state_up": True,
                     "peer_cidrs": peer_cidrs,
                     "ikepolicy_id": ikepolicy_id,
                     "dpd": {
                         "action": "hold",
                         "interval": 60,
                         "timeout": 240
                      },
                     "vpnservice_id": vpnservice_id,
                     "peer_address": peer_address,
                     "peer_id": peer_address,
                     "name": connection_name,
                     "availability_zone": az
                  }
                  }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/ipsec-site-connections'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_ipsec_vpn_connection(project_token, region, az, connection_name, ipsecpolicy_id, ikepolicy_id,
                                vpnservice_id, peer_cidrs, peer_address, psk):
    """
    Create a IPsec vpn connection.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param az: Availability zone name.
    :param connection_name: Name of VPN connection.
    :param ipsecpolicy_id: ID of IPsec policy to use.
    :param ikepolicy_id: ID of IKE policy to use.
    :param vpnservice_id: ID of VPN service to use
    :param peer_cidrs:
    :param peer_address:
    :param psk:
    :return: ID of IPsec vpn connection if succesfull. Otherwise error from requests library.
    """
    request = _rest_create_ipsec_vpn_connection(project_token, region, az, connection_name, ipsecpolicy_id, ikepolicy_id,
                                                vpnservice_id, peer_cidrs, peer_address, psk)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()['ipsec_site_connection']['id']


def _rest_list_ipsec_connections(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/ipsec-site-connections'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def list_ipsec_vpn_connections(project_token, region):
    """
    List IPsec VPN connections.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :return: JSON that contains IPsec VPN connections if succesfull. Otherwise error from requests library.

    """
    request = _rest_list_ipsec_connections(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def get_ipsec_vpn_connection_id(project_token, region, connection_name):
    """
    List IPsec VPN connections.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param connection_name: Name of VPN connection
    :return: JSON that contains IPsec VPN connections if succesfull. Otherwise error from requests library.

    """
    request = _rest_list_ipsec_connections(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()

        # Get ID of our connector from info
        outputList = []
        outputDict = request['ipsec_site_connections']

        counter = 0
        for i in outputDict:
            if str(i['name']) == connection_name:
                outputList.append(str(i['id']))
                counter += 1

        return outputList[0]


def _rest_get_delete_ipsec_vpn_connection(http_method, project_token, region, connection_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/ipsec-site-connections/' + connection_id

    try:
        if 'get' in http_method:
            request = requests.get(url, headers=headers)
        else:
            request = requests.delete(url, headers=headers)

        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def get_ipsec_vpn_connection_info(project_token, region, connection_id):
    """
    Get IPsec VPN connection detailed info.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param connection_id: ID of connection.
    :return: JSON that contains IPsec VPN connection info if succesfull. Otherwise error from requests library.

    """
    http_method = 'get'
    request = _rest_get_delete_ipsec_vpn_connection(http_method, project_token, region, connection_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def delete_ipsec_vpn_connection(project_token, region, connection_id):
    """
    Get IPsec VPN connection detailed info.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param connection_id: ID of vpn connection to be deleted.
    :return: Http 204 code if succesfull. Otherwise error from requests library.

    """
    http_method = 'delete'
    request = _rest_get_delete_ipsec_vpn_connection(http_method, project_token, region, connection_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return str(request)


def _rest_update_ipsec_vpn_connection(project_token, region, az, connection_id, connection_name, ipsecpolicy_id,
                                      ikepolicy_id, vpnservice_id, peer_cidrs, peer_address, psk):

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {"ipsec_site_connection": {
                      "psk": psk,
                      "initiator": "bi-directional",
                      "ipsecpolicy_id": ipsecpolicy_id,
                      "admin_state_up": True,
                      "peer_cidrs": peer_cidrs,
                      "ikepolicy_id": ikepolicy_id,
                      "dpd": {
                          "action": "hold",
                          "interval": 60,
                          "timeout": 240
                       },
                      "vpnservice_id": vpnservice_id,
                      "peer_address": peer_address,
                      "peer_id": peer_address,
                      "name": connection_name,
                      "availability_zone": az
     }
     }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/ipsec-site-connections/' + connection_id

    try:
        request = requests.put(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def update_ipsec_vpn_connection(project_token, region, az, connection_id, connection_name, ipsecpolicy_id, ikepolicy_id,
                                vpnservice_id, peer_cidrs, peer_address, psk):
    """
    Update a IPsec VPN service.

    :param project_token: A valid K5 project token
    :param region: K5 region name.
    :param az: Availability zone name.
    :param connection_id: ID of VPN connection to be updated.
    :param connection_name: Name of connection.
    :param ipsecpolicy_id: ID of IPsec policy.
    :param ikepolicy_id: ID of IKE policy.
    :param vpnservice_id: ID ov VPN service.
    :param peer_cidrs:
    :param peer_address:
    :param psk:
    :return:  JSON IPsec vpn service if succesfull. Otherwise error from requests library.

    """
    request = _rest_update_ipsec_vpn_connection(project_token, region, az, connection_id, connection_name, ipsecpolicy_id,
                                                ikepolicy_id, vpnservice_id, peer_cidrs, peer_address, psk)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()

###################################################################################################
#
# SSLVPN
#
###################################################################################################

def _rest_create_ssl_vpn_service(project_token, region, az, subnet_id, router_id, service_name, description, admin_state):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    configData = {'vpnservice': {
                     'availability_zone': az,
                     'subnet_id': subnet_id,
                     'router_id': router_id,
                     'name': service_name,
                     'description': description,
                     'admin_state_up': admin_state,
                 }
    }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/vpnservices'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_ssl_vpn_service(project_token, region, az, subnet_id, router_id, service_name='vpnservice',
                           description='ssl vpn service', admin_state=True):
    """Create SSL VPN service

    :param project_token: Valid K5 project token
    :param region: Valid K5 region
    :param az: Valid K5 availability zone.
    :param subnet_id: ID of the subnet.
    :param router_id: ID of the router.
    :param service_name: Name for the service. (Optional)
    :param description: Description for service (Optional)
    :param admin_state: (bool) Defaults to true. (Optional)

    :return: JSON if succesful, othervise error from request library
    """
    request = _rest_create_ssl_vpn_service(project_token, region, az, subnet_id, router_id,
                                           service_name, description, admin_state)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_create_ssl_vpn_connection(project_token, region, az, vpn_service_id, container_id, connection_name,
                                    pool_cidr, admin_state):

    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}
    """
    configData = {"ssl_vpn_v2_connection": {
         "name": connection_name,
         "client_address_pool_cidrs": pool_cidr,
         "admin_state_up": admin_state,
         "credential_id": container_id ,
         "vpnservice_id": vpn_service_id,
         "availability_zone": az,
         "protocol": "tcp",
         "floatingips": None
        }
       }
    """
    configData = {"ssl_vpn_v2_connection": {
         "name": connection_name,
         "client_address_pool_cidrs": pool_cidr,
         "admin_state_up": admin_state,
         "credential_id": container_id ,
         "vpnservice_id": vpn_service_id,
         "availability_zone": az,
         "protocol": "tcp"
        }
       }


    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/ssl-vpn-v2-connections'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_ssl_vpn_connection(project_token, region, az, vpn_service_id, container_id, connection_name='ssl vpn connection',
                                    pool_cidr=['10.0.0.0/24'], admin_state=True):
    """
    Create SSL vpn v2 connection

    :param project_token: Valid K5 project token
    :param region: Valid K5 region
    :param az: Valid K5 availability zone.
    :param vpn_service_id: ID of vpn service
    :param container_id:  ID of vpn key container
    :param connection_name: Name of connection
    :param pool_cidr: List of CIDR:s
        ::
        Example:
        ['10.0.0.0/24']

    :param admin_state: (bool) Defaults to true. (Optional)

    :return: JSON if succesfull. Otherwise error from requests library.
    """

    request = _rest_create_ssl_vpn_connection(project_token, region, az, vpn_service_id, container_id, connection_name,
                                    pool_cidr, admin_state)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_list_ssl_vpn_connections(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}


    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/ssl-vpn-v2-connections'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def list_ssl_vpn_connections(project_token, region):
    """
    List SSL VPN connections.

    :param project_token: A valid K5 project token
    :param region: K5 region

    :return: JSON if succesfull otherwise erroro from requests library.
    """

    request = _rest_list_ssl_vpn_connections(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def get_ssl_vpn_connection_id(project_token, region, connection_name):
    """
    Get ID of SSL VPN connections.

    :param project_token: A valid K5 project token
    :param region: K5 region
    :param connection_name: Name of connection.

    :return: ID of first found connection  if succesful, otherwise error from requests library
    """

    request = _rest_list_ssl_vpn_connections(project_token, region)

    if 'Error' in str(request):
        return str(request)
    else:
        request = request.json()

        # Get ID of our connectoion from json
        outputList = []
        outputDict = request['ssl_vpn_v2_connections']

        counter = 0
        for i in outputDict:
            if str(i['name']) == connection_name:
                outputList.append(str(i['id']))
                counter += 1
        if counter:
            return outputList[0]
        else:
            return 'Not found'

def _rest_delete_ssl_vpn_connection(project_token, region, connection_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/vpn/ssl-vpn-v2-connections'+ connection_id

    try:
        request = requests.delete(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('Error: ' + str(e))
        return 'Error: ' + str(e)
    else:
        return request


def delete_ssl_vpn_connection(project_token, region, connection_id):
    """
    Delete SSL VPN connection.

    :param project_token: A valid K5 project token
    :param region: K5 region
    :param connection_id: ID of Connection

    :return: HTTP 204 if succesfull otherwise error from requests library.
    """

    request = _rest_delete_ssl_vpn_connection(project_token, region, connection_id)
    if 'Error' in str(request):
        return str(request)
    else:
        return request

