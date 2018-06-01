from os import environ as env
import sys
import argparse
import json
sys.path.append('k5lib')
import k5lib


username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
region = env['OS_REGION_NAME']
projectname = env['OS_PROJECT_NAME']


# Create a log file
k5lib.create_logfile('create_keypair.log')

# Setup command line parser
parser = argparse.ArgumentParser(description="Create keypair ")
parser.add_argument("name", help="Name of the keypair")
parser.add_argument("az", help="Name of availability zone eq fi-1a")
args = parser.parse_args()

keypair_name = args.name
az_name = args.az

privatekey = keypair_name + '_priv.pem'
publickey = keypair_name + '_pub.pem'

project_token = k5lib.get_project_token(username, password, domain, projectname, region)
project_id = k5lib.get_project_id(username, password, domain, projectname, region)
keypair_info = k5lib.create_keypair(project_token,project_id, region, az_name, keypair_name )

print(json.dumps(keypair_info, indent=2))

info_dict = keypair_info['keypair']
with open(privatekey, 'w') as file:
    file.write(info_dict['private_key'])

with open(publickey, 'w') as file:
    file.write(info_dict['public_key'])

