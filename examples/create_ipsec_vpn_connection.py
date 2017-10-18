from os import environ as env
import sys
import k5lib
import logging
import json

#
# Set up enviroment
#
username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
region = env['OS_REGION_NAME']
projectName = env['OS_PROJECT_NAME']

########################################################################################################################
# Parameters
########################################################################################################################

postfix = 'vpn_example'

#
# K5 network parameters
#
az = 'fi-1b'
network_id = 'REPLACE_WITH_K5_NETWORK_ID'
subnet_id = 'REPLACE_WITH_K5_SUBNET_ID'
router_id = 'REPLACE_WITH_K5_ROUTER_ID'

#
# VPN parameters
#
site_network_1 = '10.11.10.0/24'
site_network_2 = '10.11.20.0/24'
cisco_IP = 'REPLACE_WITH_CISCO_PUBLIC_IP'
vpn_password = 'XXXXXXXXXX'

########################################################################################################################

#
# Names for components
#
vpn_service_name = 'vpn-service-' + postfix
ike_policy_name = 'ike-policy-' + postfix
ipsec_policy_name = 'ipsec-policy-' + postfix
ipsec_connection_name = 'ipsec-connection-' + postfix
ipsec_connection_name2 = 'ipsec-connection-2-' + postfix

#
# Create a log file
#
k5lib.create_logfile('create_ipsec_vpn_conection.log')

#
# Get token
#
project_token = k5lib.get_project_token(username, password, domain, projectName, region)

#
# log network & subnet & router ID:s
#
logging.info('network_id: ' + network_id)
logging.info('subnet_id: ' + subnet_id)
logging.info('router_id: ' + router_id)

#
# Create IPsec VPN service
#
vpn_service_id = k5lib.create_ipsec_vpn_service(project_token, region, az, vpn_service_name, router_id, subnet_id)
vpn_service_info = k5lib.get_ipsec_vpn_service_info(project_token, region, vpn_service_id)
logging.info('vpn_service_id: ' + vpn_service_id)
logging.info(json.dumps(vpn_service_info, indent=2))
print(json.dumps(vpn_service_info, indent=2))

#
# Create vpn IKE policy
#
ike_policy_id = k5lib.create_ike_policy(project_token, region,az, ike_policy_name, 'main', 'sha1', 'aes-256', 'group5', '7200', 'v1')
logging.info('ike_policy_id: ' + ike_policy_id)
ike_policy_info = k5lib.get_ike_policy_info(project_token, region, ike_policy_id)
logging.info(json.dumps(ike_policy_info, indent=2))
print(json.dumps(ike_policy_info, indent=2))

#
# Create vpn IPsec policy
#
ipsec_policy_id = k5lib.create_ipsec_policy(project_token,region, az, ipsec_policy_name, 'esp', 'sha1', 'tunnel', 'aes-256', 'group5', '7200')
logging.info('ipsec_policy_id: ' + ipsec_policy_id)
ipsec_policy_info = k5lib.get_ipsec_policy_info(project_token, region, ipsec_policy_id)
logging.info(json.dumps(ipsec_policy_info, indent=2))
print(json.dumps(ipsec_policy_info, indent=2))

#
# Create IPsec VPN connection 1
#
ipsec_connection_id = k5lib.create_ipsec_vpn_connection(project_token, region, az, ipsec_connection_name, ipsec_policy_id,
                                                        ike_policy_id, vpn_service_id, site_network_1, cisco_IP, vpn_password)
logging.info('ipsec_connection_id: ' + ipsec_connection_id)
vpn_connection_info = k5lib.get_ipsec_vpn_connection_info(project_token, region, ipsec_connection_id)
logging.info(json.dumps(vpn_connection_info, indent=2))
print(json.dumps(vpn_connection_info, indent=2))


#
# Create IPsec VPN connection 2
#
ipsec_connection_id2 = k5lib.create_ipsec_vpn_connection(project_token, region, az, ipsec_connection_name2, ipsec_policy_id,
                                                        ike_policy_id, vpn_service_id, site_network_2, cisco_IP, vpn_password)
logging.info('ipsec_connection_id2: ' + ipsec_connection_id2)
vpn_connection_info2 = k5lib.get_ipsec_vpn_connection_info(project_token, region, ipsec_connection_id2)
logging.info(json.dumps(vpn_connection_info2, indent=2))
print(json.dumps(vpn_connection_info2, indent=2))
