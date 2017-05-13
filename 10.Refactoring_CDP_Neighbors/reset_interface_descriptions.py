#!/usr/bin/env python

"""
This is just some code that is done within the python
interactive shell at the end of Video # 10.
"""


from __future__ import absolute_import, division, print_function

from pprint import pprint
import netmiko


switch = {'ip': '172.18.1.11', 'device_type': 'cisco_ios',
          'username': 'admin', 'password': 'automate'}


connection = netmiko.ConnectHandler(**switch)
output = connection.send_command('show run | incl ^interface')
interfaces = output.splitlines()

pprint(interfaces)


def reset_interface_descriptions(connection):
    config = []
    for interface in interfaces:
        config.append(interface)
        config.append(' no description')
        config.append('!')  # still optional
    print('\n'.join(config))
    connection.send_config_set(config)
