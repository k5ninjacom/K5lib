"""LB module.

LB module provide functions for loadbalancer service of Fujitsu K5 cloud REST API

"""
import requests
import json
import logging as log

def _rest_create_lb(project_token, region):
    headers = {'Content-Type': 'application/json',
               'Accept': 'application/json',
               'X-Auth-Token': project_token}

    url = 'https://loadbalancing.' + region + '.cloud.global.fujitsu.com/?'

    # TODO: LB is configured differently, instead of JSON workload we need to add parameters into URL

    """
      In the example below, "https://loadbalancing.(regionName).cloud.global.fujitsu.com/" is the
      endpoint, "CreateLoadBalancer" is the action, and the remainder are the parameters.

      https://loadbalancing.(regionName).cloud.global.fujitsu.com/?
      LoadBalancerName=MyLB01
      &Listeners.member.1.LoadBalancerPort=80
      &Listeners.member.1.InstancePort=80
      &Listeners.member.1.Protocol=http
      &Listeners.member.1.InstanceProtocol=http
      &Scheme=internal
      &Subnets.member.1=subnet-3561b05d
      &Version=2014-11-01
      &Action=CreateLoadBalancer       
    """


    try:
        request = requests.post(url, headers=headers)
        request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return 'Error: ' + str(e)
    else:
        return request


def create_lb(project_token, region):
    request = _rest_stub(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()
