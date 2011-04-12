#!/usr/bin/python
# Copyright (C) 2011  Rohan Jain
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>

import sys
import argparse
from paster.services import paste, SERVICES, list_details, LISTS
from paster.config import DEFAULTS

#Args parser and arguments definitions
def parse():
    parser = argparse.ArgumentParser(description='A generic pastebin tools')
    subparsers = parser.add_subparsers(title='subcommands',
                                       description='available subcommands',
                                       help='additional help')
    main_parser = subparsers.add_parser('paste',
                                        help='paste a snippet')
    main_parser.add_argument('-s', '--syntax', metavar='syntax',
                             default=DEFAULTS['syntax'],
                             help='syntax of the paste')
    main_parser.add_argument('-t', '--title', metavar='title',
                             default=DEFAULTS['title'],
                             help='title of paste')
    main_parser.add_argument('-n', '--poster', metavar='name/email ',
                             default=DEFAULTS['poster'],
                             help='name or email of poster')
    main_parser.add_argument('-v', '--service', metavar='service ',
                             default=DEFAULTS['service'],
                             choices=SERVICES.keys(),
                             help='specify the pastebin service to be used')
    main_parser.add_argument('-e', '--extra', metavar='extra ',
                             default=DEFAULTS['extra'],
                             help='specify some extra arguements (urlencoded)')
    main_parser.add_argument('-d', '--hold', action='store_true',
                             default=DEFAULTS['hold'],
                             help='delay the deletion of post')
    main_parser.add_argument('-p', '--private', action='store_true',
                             default=DEFAULTS['private'],
                             help='hold the paste (delay in deletion)')
    main_parser.add_argument('-c', '--command', action='store_true',
                             default=DEFAULTS['command'],
                             help='post output of command supplied as content')
    main_parser.add_argument('-f', '--file', action='store_true',
                             default=DEFAULTS['file'],
                             help='post output of file supplied as content')
    main_parser.add_argument('content', metavar='content', nargs=1,
                             type=str,default=[''], help='the content')
    main_parser.set_defaults(func=paste)

    list_parser = subparsers.add_parser('list',
                                        help='list various available properties')
    list_parser.add_argument('-v', '--service', metavar='service ',
                             default=DEFAULTS['service'],
                             choices=SERVICES.keys(),
                             help='specify the pastebin service to be used')
    list_parser.add_argument('type', metavar='type', nargs=1, type=str,
                             choices = LISTS.keys(),
                             help='the property to be listed')
    list_parser.set_defaults(func=list_details)

    args = parser.parse_args()
                
    #Get the paste service according to supplied argument
    try:
        args.func(vars(args))
    except KeyboardInterrupt:
        sys.exit(1)  
