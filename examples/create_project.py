from os import environ as env
import sys
import argparse
sys.path.append('k5lib')
import k5lib


username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
region = env['OS_REGION_NAME']
projectName = 'foobar_project'


# Create a log file
k5lib.create_logfile('create_project.log')

# Setup command line parser
parser = argparse.ArgumentParser(description="Create project ")
parser.add_argument("project_name", help="Name of the project")
args = parser.parse_args()

project_Name = args.project_name

regionToken = k5lib.get_region_token(username, password, domain, region)
domainId = k5lib.get_domain_id(username, password, domain)
newproject = k5lib.create_project(regionToken, domainId, region, project_Name)
print(newproject)
