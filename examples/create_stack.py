from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib
import argparse



# Create a log file
k5lib.create_logfile('create_stack.log')

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

# Setup command line parser
parser = argparse.ArgumentParser(description="Get a password of server(s) ")
parser.add_argument("templatefile", help="Template")
parser.add_argument("stackname", help="Name of the stack")
args = parser.parse_args()


templatefile = args.templatefile

projectToken = k5lib.get_project_token(username, password, domain, projectName, region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)

stackName = args.stackname

with open(templatefile, 'r') as file:
    template = file.read()
print(template)

stackInfo = k5lib.create_stack(projectToken, region, projectId, stackName, template)
print(stackInfo)
