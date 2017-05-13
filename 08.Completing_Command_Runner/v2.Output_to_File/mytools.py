from __future__ import absolute_import, division, print_function

from getpass import getpass

def get_input(prompt=''):
    try:
        line = raw_input(prompt)
    except NameError:
        line = input(prompt)
    return line


def get_credentials():
    """Prompt for and return a username and password."""
    username = get_input('Enter Username: ')
    password = None
    while not password:
        password = getpass()
        password_verify = getpass('Retype your password: ')
        if password != password_verify:
            print('Passwords do not match.  Try again.')
            password = None
    return username, password
