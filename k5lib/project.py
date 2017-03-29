import requests
import json
import logging
import k5lib.authenticate

def show (token, project_id):

    headers = {'Content-Type': 'application/json',
               'Accept' : 'application/json',
               'X-Auth-Token': token}

    configData =  {
                "project_id": project_id}
    url = "https://identity.uk-1.cloud.global.fujitsu.com/v3/projects/" + project_id

    #print (url)
    r = requests.get(url,json=configData, headers=headers)

    #print ('statuscode', r.status_code)

    return r.json()

def rest_list_projects(regionToken, domainId, region):
    headers = {'Content-Type': 'application/json',
               'Accept' : 'application/json',
               'X-Auth-Token': regionToken}

#    configData = {'domain_id': domainId,
#                  'name': domainName}

    url = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/projects?domain_id=' + domainId
#    url = 'https://identity.' + region + '.cloud.global.fujitsu.com/v3/projects?domain_id=' + domainId + ',' + domainName + ',enabled'

    try:
        r = requests.get(url, headers=headers)
#        r = requests.get(url, json=configData, headers=headers)

#        logging.info(r)

        return r
    except:
#        logging.debug(r)
#        logging.debug(r.json)
        return


def list_projects(regionToken, domainId, region):
    r = rest_list_projects(regionToken, domainId, region)
    return r.json()


def get_project_id(user, password, contract, projectName, region):
    request = k5lib.authenticate.rest_project_authenticate(user, password, contract, projectName, region)
    r = request.json()
    return r['token']['project']['id']


def get_project_info(user, password, contract, projectName, region):
    r = k5lib.authenticate.rest_project_authenticate(user, password, contract, projectName, region)
    return r.json()