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

project_token = k5lib.get_project_token(user_name, password, domain, project_name, region)
project_id = k5lib.get_project_id(user_name, password, domain, project_name, region)

# security_group_id = k5lib.get_security_group_id(project_token, region, 'sg_ext_mgmt')
k5lib.create_security_group(project_token, region, name='sg_ext_mgmt', description='external management')

security_group_id = k5lib.get_security_group_id(project_token, region, 'sg_ext_mgmt')
print (security_group_id)

rule_return_value = k5lib.create_security_group_rule(project_token, region, security_group_id, 'ingress', 'IPv4', '22', '22', ip + '/32', None)
print (rule_return_value)

security_group_list = k5lib.list_security_groups(project_token, region)
print(json.dumps(security_group_list,indent=2))
