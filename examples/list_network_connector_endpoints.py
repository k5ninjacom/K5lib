from os import environ as env
import json
import sys
sys.path.append('k5lib')
import k5lib

# Create a log file
k5lib.create_logfile('list_network_connector_endpoints.log')


username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

projectToken = k5lib.get_project_token(username, password, domain, projectName, region)
network_connections = k5lib.list_network_connector_endpoints(projectToken, region)
print(json.dumps(network_connections, indent=2))
