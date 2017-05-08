from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib

# add filemode="w" to overwrite
logging.basicConfig(filename="get_defaultproject_id.log", level=logging.DEBUG)

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']

domainId = k5lib.get_defaultproject_id(username, password, domain)
print(domainId)
