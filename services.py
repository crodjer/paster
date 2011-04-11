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

import urllib
import urllib2
import subprocess

GET = 1
POST = 2

class BasePaste(object):
    method = GET
    url = 'http://example.com/'
    title = 'Pastebin'
    data = {}    

    def __init__(self, data):
        self.data = data

    def process_content(self):
        data = self.data
        data_content = data['content'][0]
        if data['command']:
            try:
                call = subprocess.Popen(data_content.split(),
                                        stderr=subprocess.PIPE, stdout = subprocess.PIPE)
                out, err = call.communicate()
                content = out
            except OSError:
                print 'Can not execute the command'
                content = ''
                
            if not data['title']:
                data['title'] = 'Output of command: `%s`' %(data_content)
        elif data['file']:
            try:
                f = file(data_content)
                content = f.read()            
                f.close()
            except IOError:
                print 'File not present or unreadable'
                content = ''
                
            if not data['title']:
                data['title'] = 'File: `%s`' %(data_content)
        else:
            content = data_content
        self.data['content'] = content

    def process_data(self):
        return self.data
    
    def get_response(self):
        self.process_content()
        data = self.process_data()
        urlencoded_data = urllib.urlencode(self.data)
        if self.method == GET:            
            req = urllib2.Request('%s?%s' %(self.url, urlencoded_data))
        else:
            req = urllib2.Request(self.url, urlencoded_data)

        if self.data['content']:
            self.response = urllib2.urlopen(req)
        else:
            self.response = None
        return self.response

    def get_url(self):
        response = self.get_response()
        if response:
            print 'Your paste has been published at %s' %(response.url)
            return response.url
        else:
            print 'Your paste was not published'
            return None

    def __str__(self):
        return "%s: %s" %(self.title, self.url)

class Dpaste(BasePaste):
    title = 'Dpaste'
    url = 'http://dpaste.com/'
    method = POST

    def process_data(self):        
        self.data['hold'] = 'on' if self.data['hold'] else ''        
        self.data['language']= self.data['syntax']        
        return self.data

class PastebinPaste(BasePaste):
    title = 'Pastebin'
    url = 'http://pastebin.com/api/api_post.php'
    method = 'post'

    def process_data(self):                
        self.data['language']= self.data['syntax']
        del self.data['syntax']
        return self.data

dpaste = Dpaste
pastebin = PastebinPaste
