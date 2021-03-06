from os import environ as env
import sys
import json
sys.path.append('k5lib')
import k5lib

# Create a log file
k5lib.create_logfile('delete_network_connector.log')

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


connectors = k5lib.list_network_connectors(projectToken, region)
print((json.dumps(connectors, indent=2)))

# loop trough connectors and find ones with 'mhaNe' on name, then delete it
request = connectors
outputList = []
outputDict = request['network_connectors']

counter = 0
for i in outputDict:
    if 'mhaNet' in str(i['name']):
        print('deleting connector: ', str(i['name']) )
        print(k5lib.delete_network_connector(projectToken, region, str(i['id'])))
        counter += 1

print('deleted: ', counter )
