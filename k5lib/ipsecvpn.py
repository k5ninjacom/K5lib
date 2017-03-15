import requests
import json


def list_vpn_services (token):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': token}

    r = requests.get("https://networking.uk-1.cloud.global.fujitsu.com/v2.0/vpn/vpnservices",headers=headers)

    return r.json()


def list_ike_policies (token):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': token}

    r = requests.get("https://networking.uk-1.cloud.global.fujitsu.com/v2.0/vpn/ikepolicies",headers=headers)
    return r.json()


def list_ipsec_policies (token):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': token}

    r = requests.get("https://networking.uk-1.cloud.global.fujitsu.com/v2.0/vpn/ipsecpolicies",headers=headers)
    return r.json()


def list_ipsec_connections (token):

    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': token}

    r = requests.get("https://networking.uk-1.cloud.global.fujitsu.com/v2.0/vpn/ipsec-site-connections",headers=headers)
    return r.json()


def create_vpn_service (token, subnet_id, router_id, name, admin_state):
    headers = {'Content-Type': 'application/json',
               'Accept' : 'application/json',
               'X-Auth-Token': token}
    configData = {'vpnservice': {
                                'subnet_id': subnet_id,
                                'router_id': router_id,
                                'name': name,
                                'admin_state_up': admin_state
                                 }
                 }

    json.dumps(configData)
    r = requests.post("https://networking.uk-1.cloud.global.fujitsu.com/v2.0/vpn/vpnservices",json=configData, headers=headers)

    return r.json()


def create_ike_policy (token, negotation_mode, auth_algorithm, encryption_algorithm, pfs, units, value, ike_version, name):
    headers = {'Content-Type': 'application/json',
               'Accept' : 'application/json',
               'X-Auth-Token': token}
    # Defaults:
    #{
    #"ikepolicy": {
    #"phase1_negotiation_mode": "main",
    #"auth_algorithm": "sha1",
    #"encryption_algorithm": "aes-128",
    #"pfs": "group5",
    #"lifetime": {
    #"units": "seconds",
    #"value": 7200
    #},
    #"ike_version": "v1",
    #"name": "ikepolicy1"
    #}
    #}
    configData =  {
                "ikepolicy": {
                        "phase1_negotiation_mode": negotation_mode,
                        "auth_algorithm": auth_algorithm,
                        "encryption_algorithm": encryption_algorithm,
                        "pfs": pfs,
                         "lifetime": {
                            "units": units,
                            "value": value
                            },
                         "ike_version": ike_version,
                         "name": name}
                }

    r = requests.post("https://networking.uk-1.cloud.global.fujitsu.com/v2.0/vpn/ikepolicies",json=configData, headers=headers)
    return r.json()


def createIpsecpolicy (token, name,transform_protocol, auth_algorithm, encapsulation_mode, encryption_algorithm, pfs, availability_zone):
    headers = {'Content-Type': 'application/json',
               'Accept' : 'application/json',
               'X-Auth-Token': token}

    configdata={
        "ipsecpolicy": {
        "name": name,
        "transform_protocol": transform_protocol,
        "auth_algorithm": auth_algorithm,
        "encapsulation_mode": encapsulation_mode,
        "encryption_algorithm": encryption_algorithm,
        "pfs": pfs,
        "availability_zone": availability_zone}
    }

    r = requests.post("https://networking.uk-1.cloud.global.fujitsu.com/v2.0/vpn/ipsecpolicies", json=configData, headers=headers)
    return r.json()


def create_ipsec_connection (token, psk, iniator, ipsecpolicy_id, admin_state, peer_cidr, ikepolicy_id, vpn_service_id, peer_address, peer_id, name, availability_zone):
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'X-Auth-Token': token}

    #TODO should peer_cidrs be dictionary, list or similar, now we can create one network
    #TODO testing

    configdata = {
        "ipsec_site_connection": {
        "psk": psk,
        "initiator": iniator,
        "ipsecpolicy_id": ipsecpolicy_id,
        "admin_state_up": admin_state,
        "peer_cidrs": [
          peer_cidr
        ],
        "ikepolicy_id": ikepolicy_id,
        "dpd": {
          "action": "hold",
          "interval": 60,
          "timeout": 240
        },
        "vpnservice_id": vpn_service_id,
        "peer_address": peer_address,
        "peer_id": peer_id,
        "name": name,
        "availability_zone": availability_zone}
    }

    r = requests.post("https://networking.uk-1.cloud.global.fujitsu.com/v2.0/vpn/ipsec-site-connections", json=configData,
                      headers=headers)
    return r.json()


def delete_vpn_service ():
    return


def delete_ike_policy ():
    return


def delete_ipsec_policy ():
    return
