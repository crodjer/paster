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
import services

parser = argparse.ArgumentParser(description='Paste to dpaste.com')
parser.add_argument('-s', '--syntax', metavar='syntax', default="",
                    help='syntax of the paste')
parser.add_argument('-t', '--title', metavar='title', default="",
                    help='title of paste')
parser.add_argument('-n', '--poster', metavar='name/email ', default="",
                    help='name or email of poster')
parser.add_argument('-b', '--pastebin', metavar='pastebin ', default="dpaste",
                    help='specify the pastebin to be used')
parser.add_argument('-d', '--hold', default=False, action='store_true',
                    help='hold the paste (delay in deletion)')
parser.add_argument('-c', '--command', default=False, action='store_true',
                    help='post output of command supplied as content')
parser.add_argument('-f', '--file', default=False, action='store_true',
                    help='post output of file supplied as content')
parser.add_argument('content', metavar='content', nargs=1, type=str,
                    help='the content')
args = parser.parse_args()
            
data = vars(args)

paste = getattr(services, args.pastebin)(data)
paste.get_url()
