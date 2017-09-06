import requests
from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib
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

security_groups = k5lib.list_security_groups(project_token, region)
print (security_groups)
# rule_return_value = k5lib.create_security_group_rule(project_token, region, security_group_id, direction='ingress', )