from os import environ as env
import k5lib
import logging
import json

# add filemode="w" to overwrite
logging.basicConfig(filename="get_export_status.log", level=logging.DEBUG)

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

exportId = 'fb3611a9-1b7f-4b22-b7a7-02905ff9558c'

projectToken = k5lib.get_project_token(username,password,domain,projectName,region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)

exportStatus = k5lib.get_export_status(projectToken, region,exportId)
logging.info(json.dumps(exportStatus, indent = 4))
print(json.dumps(exportStatus, indent = 4))