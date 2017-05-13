#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

import json
import mytools
import netmiko
import os
import signal
import sys

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C


def get_config_from_cdp_neighbors(input_string):
    lines = input_string.splitlines()[5:]
    hostname = None
    config = []
    for line in lines:
        words = line.split()
        if len(words) == 1:
            hostname = words[0].split('.')[0]
        elif hostname is None:
            hostname = words[0].split('.')[0]
            local = ''.join(words[1:3])
            remote = ''.join(words[-2:])
            description = '_'.join((hostname, remote))
            config.append('interface ' + local)
            config.append(' description ' + description)
            config.append('!')  # totally optional
            hostname = None
        else:
            local = ''.join(words[0:2])
            remote = ''.join(words[-2:])
            description = '_'.join((hostname, remote))
            config.append('interface ' + local)
            config.append(' description ' + description)
            config.append('!')  # totally optional
            hostname = None
    return config


if len(sys.argv) < 2:
    print('Usage: cdpneighbors.py devices.json')
    exit()

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

username, password = mytools.get_credentials()

with open(sys.argv[1]) as dev_file:
     devices = json.load(dev_file)

for device in devices:
    device['username'] = username
    device['password'] = password
    try:
        print('~' * 79)
        print('Connecting to device:', device['ip'])
        print()
        connection = netmiko.ConnectHandler(**device)
        output = connection.send_command('show cdp neighbors')
        config = get_config_from_cdp_neighbors(output)
        print('\n'.join(config))
        connection.send_config_set(config)
        connection.send_command('write memory')
        connection.disconnect()
    except netmiko_exceptions as error:
        print('Failed to ', device['ip'], error)
