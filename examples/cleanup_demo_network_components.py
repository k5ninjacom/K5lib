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
k5lib.create_logfile('disconnect_network_connector_endpoint.log')

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']
az = 'fi-1a'

securityGroupId = '91630e71-2555-4dcb-a720-0dd3c643f478'
networkId ='6809bf51-a224-4f16-a77e-754c3033b1b6'


projectToken = k5lib.get_project_token(username, password, domain, projectName, region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)

#
# Disconnect ports
#
# 1. List endpoints
# 2. Select one endpoint (needs to match criteria)
# 3. Find ALL ports related to endpoint
# 4. Disconnect ALL ports from endpoint
# 5. Goto 2 until all endpoints done
#

#
# 1. List endpoints & ports
connector_endpoints = k5lib.list_network_connector_endpoints(projectToken, region)
print((json.dumps(connector_endpoints, indent=2)))

ports = k5lib.list_ports(projectToken, region)
print(json.dumps(ports, indent=2))

#
# 2. Select one endpoint (needs to match criteria)


# loop trough connectors and find ones with 'mhaNe' on name, then delete it
outputDict_a = connector_endpoints['network_connector_endpoints']
outputDict_b = ports['ports']

counter_a = 0
counter_b = 0

for i in outputDict_a:
    if 'mhaNet' in str(i['name']):
        print('Connector endpoint ID: ', str(i['network_connector_id']) )
        connectorId = str(i['network_connector_id'])
        #
        # 3. Find ALL ports related to endpoint
        for j in outputDict_b:
            if connectorId in str(j['device_id']):
                print('Disconnected port:', str(j['id']))
                # k5lib.disconnect_network_connector_endpoint(projectToken, region, str(j['network_connector_id']), str(j['id']))
                counter_b +=1
        counter_a += 1

#
# Delete ports
#
# 1. List ALL ports
# 2. Select one port  (needs to match criteria)
# 3. Delete port
# 4. Goto 2 until all ports done
#

"""
ports = k5lib.list_ports(projectToken, region)
print((json.dumps(ports, indent=2)))

# loop trough ports and find ones with 'mha' on name, then delete it
request = ports
outputList = []
outputDict = request['ports']

counter = 0
for i in outputDict:
    if 'mha' in str(i['name']):
        print('deleting port: ', str(i['name']) )
        k5lib.delete_port(projectToken, region, str(i['id']))
        counter += 1

print('deleted: ', counter )
"""

#
# Delete network connector endpoints
#
# 1. List network connectors
# 2. Select one connector (needs to match criteria)
# 3. Find ALL endpoints related to connector
# 4. Delete ALL endpoints from connector
# 5. Goto 2 until all endpoints done


#
# Delete connectors
#
# 1. List ALL connectors
# 2. Select one connectors (needs to match criteria)
# 3. Delete connector
# 4. Goto 2 until all connectors done
#



foobar = k5lib.disconnect_network_connector_endpoint(projectToken, region, endpointId, portId)