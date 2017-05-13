#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

import json
import netmiko

with open('devices.json') as dev_file:
      devices = json.load(dev_file)

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

for device in devices:
    try:
        print('~' * 79)
        print('Connecting to device:', device['ip'])
        connection = netmiko.ConnectHandler(**device)
        print(connection.send_command('show clock'))
        connection.disconnect()
    except netmiko_exceptions as e:
        print('Failed to ', device['ip'], e)
    