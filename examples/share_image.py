from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib
import argparse
import logging


# Create a log file
k5lib.create_logfile('share_image.log')

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
sharing_project_name = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

# Setup command line parser
parser = argparse.ArgumentParser(description="Share image from this project with other project")
parser.add_argument("image_name", help="Name of the image to be shared")
parser.add_argument("project_name", help="Name of the project which image is to be shared with")
args = parser.parse_args()

# Authenticate into projects
sharing_project_token = k5lib.get_project_token(username, password, domain, sharing_project_name, region)
accepting_project_token = k5lib.get_project_token(username, password, domain, args.project_name, region)

logging.info('Get ID for image: ' + args.image_name)
image_id = k5lib.get_image_id(sharing_project_token, region, args.image_name)
logging.info('Image ID: ' + image_id)

logging.info('Get ID of project: ' + args.project_name)
project_id = k5lib.get_project_id(username, password, domain, args.project_name, region)
logging.info('Project ID: ' + project_id)

# Share image with project
logging.info('Share Image: ' + image_id + 'with project: ' + project_id)
sharing_status = k5lib.share_image(sharing_project_token, region, project_id, image_id )
print(str(sharing_status))

# Accept image share
logging.info('Accept image')
accept_status = k5lib.accept_image_share(accepting_project_token, region, project_id, image_id)
print(str(accept_status))
logging.info(accept_status)