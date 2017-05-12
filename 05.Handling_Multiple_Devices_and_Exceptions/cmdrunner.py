#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

import json
import netmiko

devices = """
172.18.1.1
172.18.1.2
172.18.1.3
172.18.1.4
172.18.1.5
172.18.1.11
172.18.1.12
""".strip().splitlines()

device_type = 'cisco_ios'
username = 'admin'
password = 'automate'

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

for device in devices:
    try:
        print('~' * 79)
        print('Connecting to device:', device)
        connection = netmiko.ConnectHandler(ip=device, device_type=device_type,
                                            username=username, password=password)
        print(connection.send_command('show clock'))
        connection.disconnect()
    except netmiko_exceptions as e:
        print('Failed to ', device, e)
    