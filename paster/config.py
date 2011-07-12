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
sources = config.read(['paster.cfg', '/etc/paster.cfg',
             os.path.expanduser('~/.pastercfg')])

def get_config(section, option, allow_empty_option=True, default=""):
    '''
    Get data from configs
    '''
    try:
        value = config.get(section, option)
        if value is None or len(value) == 0:
            if allow_empty_option:
                return ""
            else:
                return default
        else:
            return value
    except ConfigParser.NoSectionError:
        return default

def getboolean_config(section, option, default=False):
    '''
    Get data from configs which store boolean records
    '''
    try:
        return config.getboolean(section, option) or default
    except ConfigParser.NoSectionError:
        return default


name = get_config('user', 'name')
email = get_config('user', 'email')

if name:
    poster = name + (' <%s>' %(email) if email else '')
else:
    poster = email

service = get_config('preferences', 'service', 'dpaste')
syntax = get_config('preferences', 'syntax')
extra = get_config('preferences', 'extra')
title = get_config('preferences', 'title')
hold = getboolean_config('preferences', 'hold')
command = getboolean_config('preferences', 'command')
readfile = getboolean_config('preferences', 'file')
private = getboolean_config('preferences', 'private')

# Set the default values
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
