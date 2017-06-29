"""image module.

Image module provide functions to image service of Fujitsu K5 cloud REST API

"""
import requests
import json
import logging
import base64
import uuid

log = logging.getLogger(__name__)


def _rest_image_export(regionToken, region, projectId, image_id, containerName):
    """_rest_image_export.

    Internal rest api function to export image into object storage

    :param regionToken:
    :param region:
    :param projectId:
    :param image_id:
    :param containerName:
    :return:

    """
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': regionToken}

    # storage_container format: "/v1/AUTH_<tenantID>/<containerNAME>"
    storage_container = '/v1/AUTH_' + projectId + '/' + containerName

    configData = {'image_id': image_id,
                  'storage_container': storage_container
                  }

    # 'https://import-export.uk-1.cloud.global.fujitsu.com/v1/imageexport'
    url = 'https://import-export.' + region + '.cloud.global.fujitsu.com/v1/imageexport'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def export_image(regionToken, region, projectId, image_id, containerName):
    """export_image.

    Export image into object storage

    :param regionToken:
    :param region:
    :param projectId:
    :param image_id:
    :param containerName:
    :return:

    """
    request = _rest_image_export(regionToken, region, projectId, image_id, containerName)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_get_export_status(projectToken, region, exportId):
    """_rest_get_export_status.

    :param projectToken:
    :param region:
    :param exportId:
    :return: json

    """
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': projectToken
               }

    # https://vmimport.uk-1.cloud.global.fujitsu.com/v1/imageexport/1b70eaf3-5afb-40f4-9b44-076b376a0bcf/status
    url = 'https://vmimport.' + region + '.cloud.global.fujitsu.com/v1/imageexport/' + exportId + '/status'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('headers:')
        log.error(headers)
        log.error('url')
        log.error(url)
        return 'Error: ' + str(e)
    else:
        return request


def get_export_status(projectToken, region, exportId):
    """get_export_status.

    :param projectToken:
    :param region:
    :param exportId:
    :return: json

    """
    request = _rest_get_export_status(projectToken, region, exportId)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_clone_vm(projectToken, projectId, region, imageName, volumeId):
    """_rest_clone_vm.

    $BLOCKSTORAGE / v2 /$PROJECT_ID / volumes /$VOLUME_ID / action - H “X - Auth - Token: $OS_AUTH_TOKEN” -H “Content - Type: application / json” -d ‘{“os - volume_upload_image”: {“container_format”:”‘$CONTAINER_FORMAT
    '”,”disk_format”:”‘$DISK_FORMAT'”, ”image_name”:”‘$NAME
    '”,”force”:’$FORCE’}}’

    """
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': projectToken
               }

    """
    ‘{
         “os - volume_upload_image”: {
              “container_format”:”‘$CONTAINER_FORMAT'”,
              ”disk_format”:”‘$DISK_FORMAT'”,
              ”image_name”:”‘$NAME'”,
              ”force”:’$FORCE’
          }
    }’

    """
    configData = {'os-volume_upload_image': {
        'image_name': imageName,
        'container_format': 'bare',
        'disk_format': 'raw',
        'force': 'true'
    }
    }

    # 'https://blockstorage.uk-1.cloud.global.fujitsu.com/v2/e6d6b965219a4b94b84a173dde0605b8'
    url = 'https://blockstorage.' + region + '.cloud.global.fujitsu.com/v2/' + projectId + '/volumes/' + volumeId + '/action'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('headers:')
        log.error(headers)
        log.error('url')
        log.error(url)
        log.error('configData:')
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def clone_vm(projectToken, projectId, region, imageName, volumeId):
    """clone_vm.

    :param projectToken:
    :param projectId:
    :param region:
    :param imageName:
    :param volumeId:
    :return:

    """
    request = _rest_clone_vm(projectToken, projectId, region, imageName, volumeId)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


# curl -X GET -s $BLOCKSTORAGE/v2/$PROJECT_ID/volumes/$VOLUME_ID
def _rest_get_image_info(projectToken, projectId, region, volumeId):
    """_rest_get_image_info.

    :param projectToken:
    :param projectId:
    :param region:
    :param volumeId:
    :return:

    """
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': projectToken
               }

    # 'https://blockstorage.uk-1.cloud.global.fujitsu.com/v2/e6d6b965219a4b94b84a173dde0605b8'
    url = 'https://blockstorage.' + region + '.cloud.global.fujitsu.com/v2/' + projectId + '/volumes/' + volumeId

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('headers:')
        log.error(headers)
        log.error('url')
        log.error(url)
        return 'Error: ' + str(e)
    else:
        return request


def get_image_info(projectToken, projectId, region, volumeId):
    """get_image_info.

    :param projectToken:
    :param projectId:
    :param region:
    :param volumeId:
    :return:

    """
    request = _rest_get_image_info(projectToken, projectId, region, volumeId)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_get_image_import_queue_status(projectToken, region):
    """_rest_get_image_import_queue_status.

    GET /v1/imageimport{?start, limit}

    """
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': projectToken
               }

    url = 'https://vmimport.' + region + '.cloud.global.fujitsu.com/v1/imageimport'

    try:
        request = requests.get(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error('headers:')
        log.error(headers)
        log.error('url')
        log.error(url)
        return 'Error: ' + str(e)
    else:
        return request


def get_image_import_queue_status(projectToken, region):
    """

    Get status of image import queue.

    :param projectToken: Valid token for default project
    :param region: Region name.
    :return: JSON if suucesfull. Otherwise error from requests library.

    """
    request = _rest_get_image_import_queue_status(projectToken, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_create_image_member(default_project_token, region, project_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': default_project_token}

    configData = {'member':  project_id
                 }

    url = 'https://image.' + region + '.cloud.global.fujitsu.com/v2/images/

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def _rest_register_image(default_project_token, region, ):
    # TODO: implemantation missing
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': default_project_token}

    encodedPassword = base64.b64encode(adminPassword)
    image_uuid = str(uuid.uuid4())

    configData = {'name':  image_name,
                  'disk_format': 'raw',
                  'container_format': 'bare',
                  'location': location,
                  'checksum': checksum,
                  'id': image_uuid,
                  'min_ram': min_ram,
                  'min_disk': min_disk,
                  'conversion': True,
                  'os_type': os_type,
                  'user_name': user_name,
                  'password': encodedPassword,
                  'domain': domain_name
                 }

    url = 'https://vmimport.' + region + '.cloud.global.fujitsu.com/v1/imageimport'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request
