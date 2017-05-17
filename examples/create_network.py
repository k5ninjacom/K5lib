from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
region = env['OS_REGION_NAME']
projectName = envenv['OS_PROJECT_NAME']
networkName = 'foobar-network'
az = 'fi-1a'

# Create a log file
k5lib.create_logfile('create_network.log')


projectToken = k5lib.get_project_token(username, password, domain, projectname, region)
network = k5lib.create_network(projectToken, region, az, networkName)
print(network)