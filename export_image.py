from os import environ as env
import k5lib
import logging
import json

# add filemode="w" to overwrite
logging.basicConfig(filename="export_image.log", level=logging.DEBUG)

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

