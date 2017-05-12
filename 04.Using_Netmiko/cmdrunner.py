#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

import json
import netmiko

connection = netmiko.ConnectHandler(ip='172.18.1.1', device_type='cisco_ios',
                                    username='admin', password='automate')

print(connection.send_command('show clock'))
connection.disconnect()
