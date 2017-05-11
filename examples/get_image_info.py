from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib

# Create a log file
k5lib.create_logfile('get_image_info.log')

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

projectToken = k5lib.get_project_token(username, password, domain, projectName, region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)

imageId = 'REPLACE WITH image ID'
containerName = 'vmexport'

imageInfo = k5lib.get_image_info(projectToken, projectId, region, imageId)
print(json.dumps(imageInfo, indent=4))
