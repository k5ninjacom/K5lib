from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib
import argparse
import datetime

#
#
#
# "ca", "server_certificate", "server_key", and "dh".


def cert_from_file(filename, key_name):
    with open(filename, 'r') as file:
        cert = file.read()

    cert_uri = k5lib.create_key(projectToken, region, projectId, key_name, key=cert,
                                expiration_date=datetime.datetime.now().year + 10, key_type='text/plain')
    print(cert_uri)
    return cert_uri


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
parser.add_argument("server_cert", help="server certificate file in PEM format")
parser.add_argument("server_key", help="server key file in PEM format")
parser.add_argument("dh", help="diffie helman key file in PEM format")

args = parser.parse_args()

ca_file = args.ca
server_cert_file = args.server_cert
server_key_file = args.server_key
dh = args.dh


projectToken = k5lib.get_project_token(username, password, domain, projectName, region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)


cert_from_file(ca_file, 'ca')
cert_from_file(server_cert_file, 'server_certificate')
cert_from_file(server_key_file, 'server_key')
cert_from_file(dh, 'dh')



