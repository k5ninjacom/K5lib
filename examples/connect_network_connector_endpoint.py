from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib

# Create a log file
k5lib.create_logfile('connect_network_connector_endpoint.log')

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']
az = 'fi-1a'
endpointName01 = 'mhaNetworkConnector-ep01'

connectorName = 'mhaNetworkConnector'

projectToken = k5lib.get_project_token(username, password, domain, projectName, region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)

networkconnectorsinfo = k5lib.list_network_connectors(projectToken, region)
print(networkconnectorsinfo)
# connectorEndpoint = k5lib.create_network_connector_endpoint(projectToken, projectId, region, az, endpointName01)
# print(connectorEndpoint)
# connectstatus = k5lib.connect_network_connector_endpoint(projectToken, region, endpointId, portId)

# print(connectstatus)