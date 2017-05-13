#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

import json
import netmiko

r1 = {'ip': '172.18.1.1',
      'device_type': 'cisco_ios',
      'username': 'admin',
      'password': 'automate'}

r2 = {'ip': '172.18.1.2',
      'device_type': 'cisco_ios',
      'username': 'admin',
      'password': 'automate'}

r3 = {'ip': '172.18.1.3',
      'device_type': 'cisco_ios',
      'username': 'admin',
      'password': 'LETMEIN123'}

r4 = {'ip': '172.18.1.4',
      'device_type': 'cisco_ios',
      'username': 'admin',
      'password': 'automate'}

sw1 = {'ip': '172.18.1.11',
       'device_type': 'cisco_ios',
       'username': 'admin',
       'password': 'automate'}

sw2 = {'ip': '172.18.1.12',
       'device_type': 'cisco_ios',
       'username': 'admin',
       'password': 'automate'}

devices = [r1, r2, r3, r4, sw1, sw2]

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
    