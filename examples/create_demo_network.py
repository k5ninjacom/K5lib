"""Demo foobar network.

Two az
Two project
Inter az and project connectors
Internal networks and subnets
Routing between networks and internet
demonetwork.png

"""
from os import environ as env
import sys
import json
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

securityGroupId = '91630e71-2555-4dcb-a720-0dd3c643f478'
networkId ='6809bf51-a224-4f16-a77e-754c3033b1b6'

endpointName01 = 'mhaNetworkConnector-ep' + k5lib.gen_passwd(6)
print(endpointName01)

connectorName = 'mhaNetworkConnector-' + k5lib.gen_passwd(6)
print(connectorName)

portName = 'mha-port-' + k5lib.gen_passwd(6)
print(portName)


projectToken = k5lib.get_project_token(username, password, domain, projectName, region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)

print('networkconnector')
# Create new connector
newConnector = k5lib.create_network_connector(projectToken, projectId, region, connectorName)
print(newConnector)

# Get ID for new connector to verify ID:s are same
networkconnectorId = k5lib.get_network_connector_id(projectToken, region, connectorName)
print(networkconnectorId)

# Get list of network connectors
networkConnectorList = k5lib.list_network_connectors(projectToken, region)
print((json.dumps(networkConnectorList, indent=2)))


print('Network connector endpoint')

# Create new connector endpoint
newconnectorEndpoint = k5lib.create_network_connector_endpoint(projectToken, projectId, region, az, endpointName01, networkconnectorId)
print(newconnectorEndpoint)

# Get ID for new connector endpoint to verify ID:s are same
connectorEnpointId = k5lib.get_network_connector_endpoint_id(projectToken, region, endpointName01)
print(connectorEnpointId)

# Get list of network connector endpoints
connectorEndpointlist = k5lib.list_network_connector_endpoints(projectToken, region)
print(json.dumps(connectorEndpointlist, indent=2))


print ('port')
# Create a new network port
newPort = k5lib.create_port_on_network(projectToken, region, az, portName, securityGroupId, networkId)
print(newPort)

# Get ID for new port to verify ID:s are the same
portId = k5lib.get_port_id(projectToken, region, portName)
print(portId)

# List ports
portList = k5lib.list_ports(projectToken, region)
print(json.dumps(portList, indent=2))


connect = k5lib.connect_network_connector_endpoint(projectToken, region, connectorEnpointId, portId)
print(json.dumps(connect, indent=2))

