#!/usr/bin/env python

"""NOTE:

This file is little different from what is seen in the videos.
Please read the comments at the end of this file.
"""

from __future__ import absolute_import, division, print_function

import json
import mytools
import netmiko
import os
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
        newdir = connection.base_prompt
        try:
            os.mkdir(newdir)
        except OSError as error:
            # FileExistsError is error # 17
            if error.errno == 17:
                print('Directory', newdir, 'already exists.')
            else:
                # re-raise the exception if some other error occurred.
                raise
        for command in commands:
            filename = command.rstrip().replace(' ', '_') + '.txt'
            filename = os.path.join(newdir, filename)
            with open(filename, 'w') as out_file:
                out_file.write(connection.send_command(command) + '\n')
        connection.disconnect()
    except netmiko_exceptions as error:
        print('Failed to ', device['ip'], error)


"""
Changes from what is seen in the videos.


Lines 45 through 53:

Handle the event that the directory already exists,
for example when running the script a second time.

Python2 will raise an OSError exception, which could have several causes.
We want to make sure the error number is "17" - file exists,
in which case we assume it is OK to use the existing directory.

Python3 will raise the more specific FileExistsError,
which is a 'child' of the OSError exception.  

Since we are attempting to write Python2/3 compatible code,
we are catching the more generic OSError exception
and then checking that the error number is 17.


Line 55:

Since we are iterating over the file contents to read in the commands,
each line in the file ends with a newline character: '\n'.
We need to strip off the '\n' and so we added the string method .rstrip()


Line 56:

In the video I used the string method 'join' to join the directory name
and filename to create a Unix/Linux compatible filepath.

Instead, here I am using the os.path.join function to join
the directory name and filename to create a OS independent filepath.  
os.path.join is aware of what operating system it runs on
and will do the right thing.

"""