#!/usr/bin/python
# Copyright (c) 2011, Rohan Jain
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, this 
#    list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice,    
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#  - Neither the name of pstr nor the names of its contributors may be used to 
#    endorse or promote products derived from this software without specific
#    prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE 
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import argparse
import urllib
import urllib2
import subprocess

parser = argparse.ArgumentParser(description='Paste to dpaste.com')
parser.add_argument('-s', '--syntax', metavar='syntax', default="",
                    help='syntax of the paste')
parser.add_argument('-t', '--title', metavar='title', default="",
                    help='title of paste')
parser.add_argument('-n', '--poster', metavar='name/email ', default="",
                    help='name or email of poster')
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

if args.hold:
    hold = 'on'
else:
    hold = ''
    
data = {
    'content': content,
    'language': args.syntax,
    'title': args.title,
    'poster': args.poster,
    'hold': hold,
}
req = urllib2.Request('http://dpaste.com/', urllib.urlencode(data))
response = urllib2.urlopen(req)
print 'Your paste is published at %s' %(response.url)
