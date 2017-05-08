from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib

# add filemode="w" to overwrite
logging.basicConfig(filename="get_image_info.log", level=logging.DEBUG)

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

projectToken = k5lib.get_project_token(username,password,domain,projectName,region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)

imageId = '31b71d81-0691-4513-8293-b9c08f5052ff'
containerName = 'vmexport'

imageInfo = k5lib.get_image_info(projectToken, projectId, region, imageId)
print(json.dumps(imageInfo, indent = 4))