import requests
import json
import logging

log = logging.getLogger(__name__)

def _rest_image_export(regionToken, region, projectId, image_id, containerName):
    """
    X-Auth-Token: String

    image_id: String
        Specify the allocated ID for the export target image.

    storage_container: String
        URL of object storage where exported VM image
       files are deployed. Specify using the following
       format: /v1/AUTH_<tenantID>/<containerNAME>

    Returns:
       json object
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
        log.error(json.dumps(configData, indent= 4))
        return 'Error: ' + str(e)
    else:
        return request


def export_image(regionToken, region, projectId, image_id, containerName):
    request = _rest_image_export(regionToken, region, projectId, image_id, containerName)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_get_export_status(projectToken, region, exportId):
    headers = {'Content-Type': 'application/json',
        'X-Auth-Token': projectToken
    }

    #https://vmimport.uk-1.cloud.global.fujitsu.com/v1/imageexport/1b70eaf3-5afb-40f4-9b44-076b376a0bcf/status
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
    request = _rest_get_export_status(projectToken, region, exportId)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


def _rest_clone_vm( projectToken, projectId, region, imageName, volumeId):
    """
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
    url = 'https://blockstorage.' + region + '.cloud.global.fujitsu.com/v2/' + projectId + '/volumes/' + volumeId +'/action'

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


def clone_vm( projectToken, projectId, region, imageName, volumeId):
    request = _rest_clone_vm( projectToken, projectId, region, imageName, volumeId)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()


#curl -X GET -s $BLOCKSTORAGE/v2/$PROJECT_ID/volumes/$VOLUME_ID
def _rest_get_image_info(projectToken, projectId, region, volumeId):
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
    request = _rest_get_image_info(projectToken, projectId, region, volumeId)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()
