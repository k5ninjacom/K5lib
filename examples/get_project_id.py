from os import environ as env
import sys
import argparse
sys.path.append('k5lib')
import k5lib

# Create a log file
k5lib.create_logfile('get_project_id.log')

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

# Setup command line parser
parser = argparse.ArgumentParser(description="Get project ID ")
parser.add_argument("project_name", help="Name of the project")
args = parser.parse_args()

project_Name = args.stackname




projectId = k5lib.get_project_id(username, password, domain, project_Name, region)
print(projectId)
