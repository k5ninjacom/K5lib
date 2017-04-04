from os import environ as env
import k5lib
import logging
import json

# add filemode="w" to overwrite
logging.basicConfig(filename="export_image.log", level=logging.DEBUG)

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

projectToken = k5lib.get_project_token(username,password,domain,projectName,region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)

imageId = '31b71d81-0691-4513-8293-b9c08f5052ff'
containerName = 'vmexport'

exportId = k5lib.export_image(projectToken, region, projectId, imageId, containerName)
print(exportId)