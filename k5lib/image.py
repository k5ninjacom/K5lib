import requests
import json
import logging
import .authenticate

def rest_image_export(regionToken, image_id, containerName ):
    headers = {'Content-Type': 'application/json',
               'Accept' : 'application/json',
               'X-Auth-Token': regionToken}

    # storage_container format: "/v1/AUTH_<tenantID>/<containerNAME>"
    storage_container = '' + tenantID +'/' + containerName

    configData = {'image_id': image_id,
                  'storage_container' : storage_container }

    # storage_container format: "/v1/AUTH_<tenantID>/<containerNAME>"

    # Url = image base url +  /v1/imageexport

    url = ''
    try:
        r = requests.post(url, json=configData, headers=headers)
        logging.info(r)

        return r
    except:
#         logging.debug(r)
#         logging.debug(r.json)
         return


def export():
    return


# k5-iaas-api-reference-foundation-service.pdf
# 1.2.6.13 Delete image
def rest_image_delete(regionToken, tenant_id, image_id):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': regionToken}

    # storage_container format: "/v1/AUTH_<tenantID>/<containerNAME>"
    storage_container = '' + tenantID + '/' + containerName


    # storage_container format: "/v1/AUTH_<tenantID>/<containerNAME>"

    # Url = image base url +  /v1/imageexport

    url =

    try:
        r = requests.post(url, json=configData, headers=headers)
        logging.info(r)

        return r
    except:
        #         logging.debug(r)
        #         logging.debug(r.json)
        return


def delete():
     return