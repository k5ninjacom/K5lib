from os import environ as env
import k5lib
import json

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']

globalToken = k5lib.get_global_token(username, password, domain)
domainId = k5lib.get_domain_id(user, password, domain)

regions = k5lib.list_regions(globalToken)

print(regions.json())
