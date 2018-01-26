from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib
import json
import logging


# Create a log file
k5lib.create_logfile('get_region_info.log')

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']

globalToken = k5lib.get_global_token(username, password, domain)

region_info = k5lib.get_region_info(globalToken, 'fi-1')

logging.info(json.dumps(region_info, indent=4))
print(json.dumps(region_info, indent=4))