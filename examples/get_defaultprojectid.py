from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib

# Create a log file
k5lib.create_logfile('get_defaultprojectid.log')

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']

domainId = k5lib.get_defaultproject_id(username, password, domain)
print(domainId)
