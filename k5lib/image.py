import requests
import json
import logging
import .authenticate


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
        return 'Error: ' + str(e)
    else:
        return request


def export_image(regionToken, region, projectId, image_id, containerName):
    request = _rest_image_export(regionToken, region, projectId, image_id, containerName)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()