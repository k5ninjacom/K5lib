import logging
import k5lib
import sys

"""
This script will create a default.rc file into current folder

export OS_USERNAME=''
export OS_PASSWORD=''
export OS_PROJECT_NAME=''
export OS_PROJECT_ID=''
export OS_AUTH_URL=''
export OS_REGION_NAME=''
export OS_VOLUME_API_VERSION=2
export OS_IDENTITY_API_VERSION=3
export OS_USER_DOMAIN_NAME=''
export OS_DEFAULT_DOMAIN=''
export OS_DOMAIN_ID=''

We need following information from user:

Username
Password
Domain (aka contract)
Project name
Region
"""
# add filemode="w" to overwrite
logging.basicConfig(filename="fillrc.log", level=logging.DEBUG)



def main():
    logging.basicConfig(filename='fillrc.log', level=logging.DEBUG)
    logging.info('Started')

    userName = input("Username: ")
    userPassword = input("Password: ")
    domainName = input("Domain: ")
    projectName = input("Project name: ")
    region = input("Region: ")
    authURL = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3'

    projectId = k5lib.get_project_id(userName, userPassword, domainName, projectName, region)
    if 'Error' in str(projectId):
        logging.info(str(projectId))
        print('Exit .. ', str(projectId))
        sys.exit()

    # Create default.rc file and write on it
    rcfile = open('default.rc', 'w')
    rcfile.write('export OS_USERNAME=\'' + userName + '\'\n')
    rcfile.write('export OS_PASSWORD=\'' + userPassword + '\'\n')
    rcfile.write('export OS_PROJECT_NAME=\'' + projectName + '\'\n')
    rcfile.write('export OS_PROJECT_ID=\'' + projectId + '\'\n')
    rcfile.write('export OS_AUTH_URL=\'' + authURL + '\' \n')
    rcfile.write('export OS_REGION_NAME=\'' + region + '\'\n')
    rcfile.write('export OS_OS_VOLUME_API_VERSION=2\n')
    rcfile.write('export OS_IDENTITY_API_VERSION=3\n')
    rcfile.write('export OS_USER_DOMAIN_NAME=\'' + domainName + '\'\n')
    rcfile.write('export OS_DEFAULT_DOMAIN=\'' + domainName + '\'\n')
    rcfile.close()

    logging.info('Finished')

if __name__ == '__main__':
    main()
