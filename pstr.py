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
import subprocess
import pastebin
import urllib
import urllib2

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

if args.command:
    f = file('/tmp/pstr_command_result.txt', 'w+')
    subprocess.call(args.content[0], stdout=f)
    f.close()
    f = file('/tmp/pstr_command_result.txt')
    content = f.read()
    f.close()    
elif args.file:
    f = file(args.content[0])
    content = f.read()
    f.close()
else:
    content = args.content[0]
              
data = {
    'content': content,
    'syntax': args.syntax,
    'title': args.title,
    'poster': args.poster,
    'hold': args.hold,
}

pbin = getattr(pastebin, args.pastebin)(data)

print 'Your paste is published at %s' %(pbin.paste())
