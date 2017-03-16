from os import environ as env
import k5lib


username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']

globalToken = k5lib.authenticate.get_global_token(username, password, domain)
domainId = k5lib.authenticate.get_domain_id(user, password, domain)
regionId = 'fi-1'

response = k5lib.contract.activate_region(globalToken, domainId, regionId)
print (response)
