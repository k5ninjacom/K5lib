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
templatefile = 'xalm_devops_tools.yml'

projectToken = k5lib.get_project_token(username, password, domain, projectName, region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)

stackName = 'devops_tools'

with open(templatefile, 'r') as file:
    template = file.read()
print (template)

stackInfo = k5lib.create_stack(projectToken, region, projectId, stackName, template)
print(stackInfo)
