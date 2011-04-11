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

import argparse
from services import get_service, SERVICES
from config import DEFAULTS

#Args parser and arguments definitions
parser = argparse.ArgumentParser(description='Paste to dpaste.com')
parser.add_argument('-s', '--syntax', metavar='syntax',
                    default=DEFAULTS['syntax'], help='syntax of the paste')
parser.add_argument('-t', '--title', metavar='title',
                    default=DEFAULTS['title'], help='title of paste')
parser.add_argument('-n', '--poster', metavar='name/email ',
                    default=DEFAULTS['poster'], help='name or email of poster')
parser.add_argument('-v', '--service', metavar='service ',
                    default=DEFAULTS['service'], choices=SERVICES.keys(),
                    help='specify the pastebin service to be used')
parser.add_argument('-e', '--extra', metavar='extra ',
                    default=DEFAULTS['extra'],
                    help='specify some extra arguements (urlencoded)')
parser.add_argument('-d', '--hold', action='store_true',
                    default=DEFAULTS['hold'],
                    help='delay the deletion of post')
parser.add_argument('-l', '--list-syntax', action='store_true',  
                    help='list the available syntax for the service')
parser.add_argument('-p', '--private', action='store_true',
                    default=DEFAULTS['private'],
                    help='hold the paste (delay in deletion)')
parser.add_argument('-c', '--command', action='store_true',
                    default=DEFAULTS['command'],
                    help='post output of command supplied as content')
parser.add_argument('-f', '--file', action='store_true',
                    default=DEFAULTS['file'],
                    help='post output of file supplied as content')
parser.add_argument('content', metavar='content', nargs=1, type=str,
                    default=[''], help='the content')
args = parser.parse_args()
            
#Get the paste service according to supplied argument
paste = get_service(args.service)(vars(args))
paste.url()
