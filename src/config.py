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
'''
Parses the config settings to provide default post data info. Available and
default configs:
[user]
name = 
email = 

[preferences]
syntax =
extra =
title =
service = dpaste
hold = false
command = false
file = false
private = false
'''

import os
import ConfigParser

config = ConfigParser.ConfigParser()
config.read(['configs/default.cfg', 'configs/pastebin.cfg', '/etc/paster.cfg',
             os.path.expanduser('~/.pastercfg')])

name = config.get('user', 'name')
email = config.get('user', 'email')

if name:
    poster = name + (' <%s>' %(email) if email else '')
else:
    poster = email

service = config.get('preferences', 'service')
syntax = config.get('preferences', 'syntax')
extra = config.get('preferences', 'extra')
title = config.get('preferences', 'title')
hold = config.getboolean('preferences', 'hold')
command = config.getboolean('preferences', 'command')
readfile = config.getboolean('preferences', 'file')
private = config.getboolean('preferences', 'private')

DEFAULTS = {
    'poster': poster,
    'service': service,
    'syntax': syntax,
    'title': title,
    'hold': hold,
    'command': command,
    'file': readfile,
    'private': private,
    'extra': extra,
}
