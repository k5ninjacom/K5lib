from os import environ as env
import k5lib
import logging

# add filemode="w" to overwrite
logging.basicConfig(filename="list_regions.log", level=logging.DEBUG)

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']

globalToken = k5lib.get_global_token(username, password, domain)
regions = k5lib.list_regions(globalToken)

print(regions)
