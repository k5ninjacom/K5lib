import requests
import json
import logging

log = logging.getLogger(__name__)


def _rest_stub(projectToken, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': projectToken}

    configData = {'key1': {
                     'key2': [
                          {
                              'key3': 'value3'
                          }
                     ]
                 }
    }

    url = url = 'https://foobar.' + region + '.cloud.global.fujitsu.com/v2.0/ports'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def stub(projectToken, region):
    request = _rest_stub(projectToken, region)
    if 'Error' in str(request):
        return str(request)
    else:
        r = request.json()
        return r


def _rest_create_network_connector(projectToken, projectid, connectorName, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': projectToken}

    configData = {"network_connector": {
                     "name": connectorName,
                     "tenant_id": projectid}
    }

    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/network_connectors'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def create_network_connector(projectToken, projectid, connectorName, region):
    request =     k5lib._rest_create_network_connector(projectToken, projectid, connectorName, region)
    if 'Error' in str(request):
        return str(request)
    else:
        r = request.json()
        return r


def _rest_create_port(projecttoken, networkNamename, networkIdid, securitygroupId, az, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': projectToken}

    configData = {"port":
                                       {"network_id": networkIdid,
                                        "name": networkNamename,
                                        "admin_state_up": True,
                                        "availability_zone": az,
                                        "security_groups": [sg_id]
                                        }
    }



    url = 'https://networking.' + region + '.cloud.global.fujitsu.com/v2.0/ports'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def _rest_create_inter_project_connection(projectToken, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': projectToken}

    configData = {'key1': {
                     'key2': [
                          {
                              'key3': 'value3'
                          }
                     ]
                 }
    }

    url = url = 'https://foobar.' + region + '.cloud.global.fujitsu.com/v2.0/ports'

    try:
        request = requests.post(url, json=configData, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Whoops it wasn't a 200
        log.error(json.dumps(configData, indent=4))
        return 'Error: ' + str(e)
    else:
        return request


def inter_project_connection_create(k5token, router, port, region):

    routerURL = 'https://networking-ex.' + region + \
        '.cloud.global.fujitsu.com/v2.0/routers/' + \
        router + '/add_cross_project_router_interface'
    try:
        response = requests.put(routerURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'},
                                json={"port_id": port})
        return response
    except:
return ("\nUnexpected error:", sys.exc_info())


def update_router_routes(k5token, routerid, routes, region):
    # e.g. routes =  [{'destination': '192.168.10.0/24', 'nexthop': u'192.168.100.2'}, {'destination': '192.168.11.0/24', 'nexthop': u'192.168.100.2'}]
    try:
        routerURL = 'https://networking-ex.' + region + \
            '.cloud.global.fujitsu.com/v2.0/routers/' + routerid
        response = requests.put(routerURL,
                                headers={'X-Auth-Token': k5token,
                                         'Content-Type': 'application/json'},
                                json={"router": {"routes": routes}})
        return response
    except:
return ("\nUnexpected error:", sys.exc_info())
