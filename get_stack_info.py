from os import environ as env
import k5lib
import logging
import json

# add filemode="w" to overwrite
logging.basicConfig(filename="get_stack_info.log", level=logging.DEBUG)

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

projectToken = k5lib.get_project_token(username, password, domain, projectName, region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)

stackName = 'devops_tools'
stackId = '3c9a1b7c-f3a8-4996-aacb-4742e5c0b218'

stackInfo = k5lib.get_stack_info(projectToken, projectId, region, stackName, stackId)

logging.info(json.dumps(stackInfo, indent=4))
# print(json.dumps(stackInfo, indent = 4))
print(stackInfo)
