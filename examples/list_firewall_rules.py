from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib

# Create a log file
k5lib.create_logfile('list_firewall_rules.log')

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

projectToken = k5lib.get_project_token(username, password, domain, projectName, region)
fw_rules = k5lib.list_firewall_rules(projectToken, region)

print(fw_rules)
