from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib

# Create a log file
k5lib.create_logfile('get_vnc_console.log')

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

projectToken = k5lib.get_project_token(username, password, domain, projectName, region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)

serverId = '8928b9ba-7571-4948-8c0c-e1445f4fe75a'

vncUrl = k5lib.get_vnc_console_url(projectToken, projectId, region, serverId)

print(vncUrl)