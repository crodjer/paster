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

GET = 1
POST = 2

class BasePastebin(object):
    method = GET
    url = 'http://example.com/'
    title = 'Pastebin'
    data = {}

    def __init__(self, data):
        self.data = data

    def process_data(self):
        return self.data
    
    def get_response(self):
        data = self.process_data()
        urlencoded_data = urllib.urlencode(self.data)
        if self.method == GET:            
            req = urllib2.Request('%s?%s' %(self.url, urlencoded_data))
        else:
            req = urllib2.Request(self.url, urlencoded_data)

        self.response = urllib2.urlopen(req)        
        return self.response    

    def paste(self):
        response = self.get_response()
        return response.url

    def __str__(self):
        return "%s: %s" %(self.title, self.url)

class Dpaste(BasePastebin):
    title = 'Dpaste'
    url = 'http://dpaste.com/'
    method = POST

    def process_data(self):        
        if self.data['hold']:
            self.data['hold'] = 'on'
        else:
            self.data['hold'] = ''
        self.data['language']= self.data['syntax']
        del self.data['syntax']
        return self.data

class Dpaste(BasePastebin):
    title = 'Dpaste'
    url = 'http://pastebin.com/api/api_post.php'
    method = 'post'

    def process_data(self):                
        self.data['language']= self.data['syntax']
        del self.data['syntax']
        return self.data
dpaste = Dpaste
