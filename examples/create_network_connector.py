from os import environ as env
import k5lib
import logging
import json


# add filemode="w" to overwrite
logging.basicConfig(filename="create_stack.log", level=logging.DEBUG)

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

