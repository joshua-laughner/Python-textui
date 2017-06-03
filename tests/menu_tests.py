#!/usr/bin/env python
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from __builtin__ import int

from .context import pytui
from pytui import uibuilder

import argparse
import sys

def shell_error(msg, exit_code=1):
    print(msg, sys.stderr)
    exit(exit_code)


def one_level_menu():
    menu1 = uibuilder.Menu('Main menu')
    uibuilder.Program(menu1)


def two_level_menu():
    menu1 = uibuilder.Menu('Main menu')
    menu2a = menu1.add_submenu('Do things')
    menu2a.attach_custom_fxn('Say hello', lambda: print('Hello world!'))
    menu2a.attach_custom_fxn('Say goodbye', lambda: print('Goodbye world :('))
    menu2b = menu1.add_submenu('Do other things')
    uibuilder.Program(menu1)


test_pgrms = {'1lev': one_level_menu, '2lev':two_level_menu}
def get_args():
    allowed_pgrms = ', '.join(test_pgrms.keys())
    parser = argparse.ArgumentParser(description='Start one of the menu test programs')
    parser.add_argument('pgrm', help='Which test program to run. Possible options are: {}'
                        .format(allowed_pgrms))

    args = parser.parse_args()

    try:
        pgrm = test_pgrms[args.pgrm]
    except KeyError:
        shell_error('Program name "{}" unknown, valid names are {}'.format(
            args.pgrm, allowed_pgrms
        ))

    return pgrm


def main():
    pgrm = get_args()
    pgrm()
    exit(0)

main()
