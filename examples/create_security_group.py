from os import environ as env
import sys
import logging
sys.path.append('k5lib')
import k5lib

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
region = env['OS_REGION_NAME']
projectName = env['OS_PROJECT_NAME']
securityGroupName = 'foobar-security-group-' + k5lib.gen_passwd(6)
az = 'fi-1a'

# Create a log file
k5lib.create_logfile('create_security_group.log')

project_token = k5lib.get_project_token(username, password, domain, projectName, region)
securityGroupId = k5lib.create_security_group(project_token, region, securityGroupName, 'Testgroup' )
logging.info('Security group ID: ' + securityGroupId)
print('Security group ID: ', securityGroupId)

securityGroupRuleId = k5lib.create_security_group_rule(project_token, region, securityGroupId, 'ingress', 'IPv4', 'tcp', '8080', '8080', '0.0.0.0/0',  None)
logging.info('Security group rule ID: ' + securityGroupRuleId)
print('Security group rule ID: ', securityGroupRuleId)
