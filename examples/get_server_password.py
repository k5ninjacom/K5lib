from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib
import logging
import json
import subprocess
import argparse
import os

# Create a log file
k5lib.create_logfile('get_server_password.log')

# Setup command line parser
parser = argparse.ArgumentParser(description="Get a password of server(s) ")
parser.add_argument("keyfile", help="Private key file")
parser.add_argument("server", nargs='?', help="Server name")
parser.add_argument("-a", "--all", help="Get password of all servers on project", action="store_true")
args = parser.parse_args()

# setup enviroment
username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

# Init variables
keyfilename = args.keyfile
project_token = k5lib.get_project_token(username, password, domain, projectName, region)
project_id = k5lib.get_project_id(username, password, domain, projectName, region)
serverList = k5lib.list_servers(project_token, region, project_id)

logging.info(json.dumps(serverList, indent=2))

# Loop servers and get password
servercount=0
outputDict = serverList['servers']
for i in outputDict:
    if (str(args.server) in str(i['name']) or args.all):
        servercount=+1
        password_hash = k5lib.get_server_password(project_token, region, project_id, str(i['id']))
        with open('hashfile.temp', 'wb') as file:
            file.write(password_hash)
        file.close()
        # Decode password hash with openssl using private key file
        password = subprocess.getoutput('openssl rsautl -decrypt -inkey ' + keyfilename +' -in hashfile.temp')
        if 'error' in str(password):
            password = 'Invalid key file'

        logging.info(str(i['name']) + ': ' + password)
        print(str(i['name']) + ': ' + password)

if servercount < 1:
    print('Server not found.')
if os.path.exists('hashfile.temp'):
    os.remove('hashfile.temp')
