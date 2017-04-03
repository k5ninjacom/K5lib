from os import environ as env
import k5lib
import logging

# add filemode="w" to overwrite
logging.basicConfig(filename="get_project_id.log", level=logging.DEBUG)

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']
templatefile = 'foobar.yml'

projectToken = get_project_token(username, password, domain, projectName, region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)


stackName = 'Foobar'

with open(templatefile, 'r') as file:
    template = file.read()

stackInfo = create_stack(projectToken, region, projectId, stackName, template)
print(stackinfo.json())