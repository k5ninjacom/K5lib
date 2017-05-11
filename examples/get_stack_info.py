from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib

# Create a log file
k5lib.create_logfile('get_stack_info.log')


username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

projectToken = k5lib.get_project_token(username, password, domain, projectName, region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)

stackName = 'REPLACE WITH STACK NAME'
stackId = 'REPLACE WITH STACK ID'

stackInfo = k5lib.get_stack_info(projectToken, projectId, region, stackName, stackId)

logging.info(json.dumps(stackInfo, indent=4))
print(json.dumps(stackInfo, indent=4))

stackOutput = stackInfo["stack"]["outputs"]

file = open('private.key', 'w')

outputList = []
outputDict = stackInfo["stack"]["outputs"]

counter = 0
for i in outputDict:
    if str(i['output_key']) == 'app_private_key':
        file.write(str(i['output_value']))
        outputList.append(str(i['output_value']))
        counter += 1

print(outputList)
