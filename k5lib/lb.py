"""LB module.

LB module provide functions for loadbalancer service of Fujitsu K5 cloud REST API

"""
import requests
import json
import logging as log

"""
Load Balancer API list

Item    API                                         Description
1       ApplySecurityGroupsToLoadBalancer           Associates one or more security groups with the load balancer
2       AttachLoadBalancerToSubnets                 Attaches one or more subnets to the load balancer
3       ConfigureHealthCheck                        Specifies the health check settings to use when evaluating the
                                                    health state of the distribution destination instances of the
                                                    specified load balancer
4       CreateLBCookieStickinessPolicy              Generates a session stickiness policy
5       CreateLoadBalancer                          Creates a load balancer
6       CreateLoadBalancerListeners                 Creates one or more listeners for the port specified in the load balancer
7       CreateLoadBalancerPolicy                    Creates a policy including required attributes according to its type
8       CreateSorryServerRedirectionPolicy          Creates a policy for redirecting to the SorryServer when unable
                                                    to distribute due to the distribution destination instances
                                                    not all being in an active state.
9       DeleteLoadBalancer                          Deletes the specified load balancer
10      DeleteLoadBalancerListeners                 Deletes a listener of the specified port number from the load balancer
11      DeleteLoadBalancerPolicy                    Deletes a specified policy from the load balancer
12      DeregisterInstancesFromLoadBalancer         Deletes the specified instance from the load balancer
13      DescribeLoadBalancerAttributes              Retrieves attribute information of the load balancer that was created
14      DescribeLoadBalancerPolicies                Retrieves policy information from the load balancer
15      DescribeLoadBalancers                       Retrieves detailed information of the load balancer that was created
16      DetachLoadBalancerFromSubnets               Detaches the subnets from the load balancer
17      ModifyLoadBalancerAttributes                Changes attribute information of the specified load balancer
18      RegisterInstancesWithLoadBalancer           Adds an instance to the load balancer
19      SetLoadBalancerListenerSSLCertificate       Sets the certificate of the end of SSL communications for the specified listener
20      SetLoadBalancerPoliciesOfListener           Registers, deregisters, and changes policies that are applied to a listener of
                                                    the load balancer
"""


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
    """
    Create Load Balancer

    :param project_token: Valid K5 project token
    :param region: Valid K5 region
    :return:
    """
    request = _rest_stub(project_token, region)
    if 'Error' in str(request):
        return str(request)
    else:
        return request.json()
