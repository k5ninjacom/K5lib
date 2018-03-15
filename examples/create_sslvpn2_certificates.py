from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib
import argparse
import datetime



# Create a log file
k5lib.create_logfile('create_sslvpn2_certificates.log')

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

# Setup command line parser
parser = argparse.ArgumentParser(description="Create certificates for ssl vpn v2")
parser.add_argument("ca", help="CA file in PEM format")
parser.add_argument("xxxx", help="xxxx file in PEM format")
parser.add_argument("xxyy", help="xxyy file in PEM format")
args = parser.parse_args()


ca_file = args.ca

projectToken = k5lib.get_project_token(username, password, domain, projectName, region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)

with open(ca_file, 'r') as file:
    ca_cert = file.read()

ca_uri = k5lib.create_key(projectToken, region, projectId, key_name = 'ca', key = ca_cert,
                          expiration_date = datetime.datetime.now().year+10 , key_type = 'text/plain')
print(ca_uri)
