import requests
import json
import logging


# List regions
def rest_list_regions(globalToken):
    headers = {'Content-Type': 'application/json',
               'Accept' : 'application/json',
               'X-Auth-Token': globalToken}

    url = 'https://identity.gls.cloud.global.fujitsu.com/v3/regions'

    try:
        r = requests.get(url, headers=headers, verify=False)

#        logging.info(r)

        return r
    except:
#        logging.debug(r)
#        logging.debug(r.json)
        return


def list_regions(domainToken):

    request = rest_list_regions(domainToken)
    r = request.json()

    return r
# Todo: Find a method to return region list instead of full json
#    return r['token']['user']['domain']['id']


# Show region
def rest_show_region(domainToken, regionId):
    headers = {'Content-Type': 'application/json',
               'Accept' : 'application/json',
               'X-Auth-Token': domainToken}

    url = 'https://identity.gls.cloud.global.fujitsu.com/v3/regions/' + regionId

    try:
        r = requests.get(url, headers=headers)

        logging.info(r)

        return r
    except:
        logging.debug(r)
        logging.debug(r.json)
        return

def show_region(domainToken, regionId):

    request = rest_show_region(domainToken, regionId)
    r = request.json()

    return r


# https:// contract.gls.cloud.global.fujitsu.com
# POST /v1/contracts/{domain_id}?action=startRegion
def rest_activate_region(domainToken, domainId, regionId):
    headers = {'Content-Type': 'application/json',
               'X-Auth-Token': domainToken}

    configData = {'contract': {
                     'regions': [
                          {
                              'id': regionId
                          }
                     ]
                 }
    }

    url = 'https:// contract.gls.cloud.global.fujitsu.com/v1/contracts/' + domainId +'?action=startRegion'

    try:
        r = requests.post(url, json=configData, headers=headers)
        return r

    except:
        return r


def activate_region(domainToken, domainId, regionId):
    request = rest_activate_region(domainToken, domainId, regionId)
    r = request.json()
    return r

