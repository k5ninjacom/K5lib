import requests
from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib
import json
import time

user_name = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
region = env['OS_REGION_NAME']
project_name = env['OS_PROJECT_NAME']


r = requests.get(r'http://jsonip.com')
ip = r.json()['ip']
print ('Your IP is', ip)

# Get token for authentication
project_token = k5lib.get_project_token(user_name, password, domain, project_name, region)

# Get ID of security group we want to modify
security_group_id = k5lib.get_security_group_id(project_token, region, 'sg_ext_mgmt')
print (security_group_id)

# Add ssh access rule with current IP address
rule_return_value = k5lib.create_security_group_rule(project_token, region, security_group_id, direction='ingress',
                                                     protocol='tcp', port_range_max=22, port_range_min=22,
                                                     remote_ip_prefix=ip + '/32', remote_group_id=None)
print (rule_return_value)

