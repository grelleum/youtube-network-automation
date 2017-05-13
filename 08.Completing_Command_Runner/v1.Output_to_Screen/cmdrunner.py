#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

import json
import netmiko
import mytools
import signal
import sys

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C


if len(sys.argv) < 3:
    print('Usage: cmdrunner.py commands.txt devices.json')
    exit()

netmiko_exceptions = (netmiko.ssh_exception.NetMikoTimeoutException,
                      netmiko.ssh_exception.NetMikoAuthenticationException)

username, password = mytools.get_credentials()

with open(sys.argv[1]) as cmd_file:
    commands = cmd_file.readlines()

with open(sys.argv[2]) as dev_file:
     devices = json.load(dev_file)

for device in devices:
    device['username'] = username
    device['password'] = password
    try:
        print('~' * 79)
        print('Connecting to device:', device['ip'])
        connection = netmiko.ConnectHandler(**device)
        for command in commands:
            print('## Output of ' + command)
            print(connection.send_command(command))
            print()
        connection.disconnect()
    except netmiko_exceptions as e:
        print('Failed to ', device['ip'], e)
    