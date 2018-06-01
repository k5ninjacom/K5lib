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
k5lib.create_logfile('import_keypair.log')

# Setup command line parser
parser = argparse.ArgumentParser(description="Create keypair ")
parser.add_argument("name", help="Name of the keypair")
parser.add_argument("az", help="Name of availability zone eq fi-1a")
parser.add_argument("public_key_file", help="Public key file for import")
args = parser.parse_args()

keypair_name = args.name
az_name = args.az

project_token = k5lib.get_project_token(username, password, domain, projectname, region)
project_id = k5lib.get_project_id(username, password, domain, projectname, region)

with open(args.public_key_file, 'r') as file:
    public_key = file.read()

print('Importing key')
print(public_key)

keypair_info = k5lib.import_keypair(project_token,project_id, region, az_name, keypair_name, public_key)

# Check if keypair import was succesful
if not 'Error' in keypair_info:
    print('Created keypair: ')
    print(json.dumps(keypair_info, indent=2))
else:
    print('Error in keypair creation')