from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib
import logging
import json

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
region = env['OS_REGION_NAME']

# Create a log file
k5lib.create_logfile('list_projects.log')

regionToken = k5lib.get_region_token(username, password, domain, region)
domainId = k5lib.get_domain_id(username, password, domain)
project_list = k5lib.list_projects(regionToken, domainId, region)

logging.info(json.dumps(project_list, indent=4))
print(json.dumps(project_list, indent=4))
