from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib
import json

########################################################################################################################
# Parameters
########################################################################################################################
# Change these according your enviroment
az = 'fi-1a'
server_name = 'Dedicatet_server-' + k5lib.gen_passwd(6)
flavor_name = 'S-2'
keypair_name = 'keypair'
security_group_name = 'default'
image_name = 'Windows Server 2012 R2 SE 64bit (English) 02'
disk_size = '100'
network_name = 'network'


########################################################################################################################
# Actions ..
########################################################################################################################
# Create a log file
k5lib.create_logfile('create_server.log')

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

project_token = k5lib.get_project_token(username, password, domain, projectName, region)
project_id = k5lib.get_project_id(username, password, domain, projectName, region)
flavor_id = k5lib.get_flavor_id(project_token,region, project_id,flavor_name)
image_id = k5lib.get_image_id(project_token,region, image_name)
network_id = k5lib.get_network_id(project_token, region, network_name)

# Create server
server_create_status = k5lib.create_server(project_token, region, az, project_id, server_name, keypair_name,
                                security_group_name, flavor_id, image_id, disk_size, network_id)
print(json.dumps(server_create_status, indent=4))

# Fetch information of newly created server
server_id = server_create_status['server']['id']
server_info = k5lib.get_server_info(project_token, region, project_id, server_id)
print(json.dumps(server_info, indent=2))


