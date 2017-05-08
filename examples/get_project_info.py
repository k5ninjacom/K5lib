from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib

# add filemode="w" to overwrite
logging.basicConfig(filename="get_project_info.log", level=logging.DEBUG)

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

projectInfo = k5lib.get_project_info(username, password, domain, projectName, region)
print(json.dumps(projectInfo, indent = 2))
