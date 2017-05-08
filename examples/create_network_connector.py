from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib

# Create a log file
k5lib.create_logfile('create_network_connector.log')

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

connectorName = 'mhaNetworkConnector'

projectToken = k5lib.get_project_token(username, password, domain, projectName, region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)


connectorId = k5lib.create_network_connector(projectToken, projectId, connectorName, region)
print(connectorId)

