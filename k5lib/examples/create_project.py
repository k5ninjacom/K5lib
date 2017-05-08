from os import environ as env
import k5lib

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
region = env['OS_REGION_NAME']
projectName = 'foobar'


# Create a log file
k5lib.create_logfile('create_project.log')


regionToken = k5lib.get_region_token(username, password, domain, region)
domainId = k5lib.get_domain_id(username, password, domain)
newproject = k5lib.create_project(regionToken, domainId, region, projectName)
print(newproject)
