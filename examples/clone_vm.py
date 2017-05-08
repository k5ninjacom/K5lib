from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib

# add filemode="w" to overwrite
logging.basicConfig(filename="clone_vm.log", level=logging.DEBUG)

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

projectToken = k5lib.get_project_token(username,password,domain,projectName,region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)

volumeId = '31b71d81-0691-4513-8293-b9c08f5052ff'
imageName = 'mgmt_exported_OS'

imageId = k5lib.clone_vm( projectToken, projectId, region, imageName, volumeId)
print(imageId)