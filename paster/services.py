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
import logging

from paster.config import get_config, getboolean_config, DEFAULTS

GET = 1
POST = 2

#Available services dictionary
SERVICES = {
}

def register_service(name, Service):
    '''
    Register a pastebin service to the dictionary
    '''
    SERVICES[name] = Service

def get_service(data):
    return SERVICES[data['service']](data)

def paste(data):
    #Called for sub-method `paste`
    service = get_service(data)
    return service.url()

class PasteException(Exception): pass
       
class BasePaste(object):
    '''
    A base paste. Pastes directly based on the data from parsed args.
    Override methods and define different constants for custom results
    '''
    URL = 'http://example.com/'
    TITLE = 'Pastebin'
    METHOD = POST
    #Dictionary of available syntax
    SYNTAX_DICT = {
    }
    
    data = {}    

    def __init__(self, data):
        self.data = data

    def list_syntax(self):
        '''
        Prints a list of available syntax for the current paste service
        '''
        logging.info('Available syntax for %s:' %(self))
        for key in self.SYNTAX_DICT.keys():
            logging.info('\t%-20s%-30s' %(key, self.SYNTAX_DICT[key]))
            
    def process_commmon(self):
        '''
        Some data processing common for all services.
        No need to override this.
        '''
        data = self.data
        data_content = data['content'][0]

        if data['command']:
            try:
                call = subprocess.Popen(data_content.split(),
                                        stderr=subprocess.PIPE,
                                        stdout = subprocess.PIPE)
                out, err = call.communicate()
                content = out
            except OSError:
                logging.exception('Cannot execute the command')
                content = ''
                
            if not data['title']:
                data['title'] = 'Output of command: `%s`' %(data_content)
        elif data['file']:
            try:
                f = file(data_content)
                content = f.read()            
                f.close()
            except IOError:
                logging.exception('File not present or unreadable')
                content = ''
                
            if not data['title']:
                data['title'] = 'File: `%s`' %(data_content)
        else:
            content = data_content

        self.data['content'] = content

        if not self.SYNTAX_DICT.get(self.data['syntax'], False):
            self.data['syntax'] = ''
            

    def process_data(self):
        '''
        Override this method for custom processing of data according to the
        servicel
        '''
        return self.data

    def get_response(self):
        '''
        Returns response according submitted the data and method.
        '''
        self.process_commmon()
        data = self.process_data()
        urlencoded_data = urllib.urlencode(self.data)
        if self.METHOD == POST:
            req = urllib2.Request(self.URL, urlencoded_data)
        else:
            req = urllib2.Request('%s?%s' %(self.URL, urlencoded_data))

        if not self.data['content']:
            raise PasteException("No content to paste")

        self.response = urllib2.urlopen(req)
        return self.response

    def process_response(self):
        '''
        Override this method for a custom procesing of response. In case the
        response url is required as paste url, no need to override this.
        '''        
        raise PasteException("Not implemented")

    def url(self):
        '''
        Executes the methods to send request, process the response and then
        publishes the url.
        '''
        self.get_response()
        url = self.process_response()
        
        if url:
            logging.info('Your paste has been published at %s' %(url))
            return url
        else:
            logging.error('Did not get a URL back for the paste')
            raise PasteException("No URL for paste")

    def __str__(self):
        return "%s" %(self.TITLE)

class Dpaste(BasePaste):
    '''
    The django based `dpaste.com` paste service
    '''
    TITLE = 'Dpaste'
    URL = 'http://dpaste.com/'
    SYNTAX_DICT = {
        'Xml': 'XML', 'Python': 'Python', 'Rhtml': 'Ruby HTML (ERB)',
        'PythonConsole': 'Python Interactive/Traceback',
        'JScript': 'JavaScript', 'Haskell': 'Haskell',
        'Bash': 'Bash script', 'Sql': 'SQL', 'Apache': 'Apache Config',
        'Diff': 'Diff', 'Ruby': 'Ruby', 'DjangoTemplate': 'Django Template/HTML',
        'Css': 'CSS'
    }

    def process_data(self):
        self.data['hold'] = 'on' if self.data['hold'] else ''
        self.data['language']= self.data['syntax']
        return self.data

class PastebinPaste(BasePaste):
    '''
    A paste for pastebin. Supports pastebin api V3.
    Available configs (edit in ~/.pastercfg):
        [pastebin]
        api_dev_key =
        api_paste_expire_date =
        api_user_name =
        api_user_password =
    '''

    TITLE = 'Pastebin'
    URL = 'http://pastebin.com/api/api_post.php'
    SYNTAX_DICT = {
        'c_loadrunner': 'C:Loadrunner', 'c_mac': 'CforMacs', 'gambas': 'GAMBAS',
        'purebasic': 'PureBasic', 'pic16': 'Pic16', 'text': 'None',
        'klonec': 'CloneC', 'abap': 'ABAP', 'pixelbender': 'PixelBender',
        'csharp': 'C#', 'go': 'Go', 'php-brief': 'PHPBrief',
        'gwbasic': 'GwBasic', 'xml': 'XML', 'lb': 'LibertyBASIC',
        'z80': 'Z80Assembler', 'gml': 'GameMaker', 'xbasic': 'XBasic',
        'fortran': 'Fortran', 'matlab': 'MatLab', 'ada': 'Ada',
        'mmix': 'MIXAssembler', 'erlang': 'Erlang', 'reg': 'REG',
        'bnf': 'BNF', 'jquery': 'jQuery', 'genero': 'Genero', 'plsql': 'PL/SQL',
        'python': 'Python', 'hq9plus': 'HQ9Plus', 'zxbasic': 'ZXBasic',
        'falcon': 'Falcon', 'd': 'D', 'lisp': 'Lisp', 'gdb': 'GDB',
        'providex': 'ProvideX', 'unicon': 'Unicon', 'perl6': 'Perl6',
        '6502tasm': '6502TASM/64TASS', 'systemverilog': 'SystemVerilog',
        '6502acme': '6502ACMECrossAssembler', 'div': 'DIV', 'kixtart': 'KiXtart',
        'fsharp': 'F#', 'cfm': 'ColdFusion', 'vhdl': 'VHDL', 'rsplus': 'R',
        'lolcode': 'LOLCode', 'mysql': 'MySQL', 'freebasic': 'FreeBasic',
        'lsl2': 'LindenScripting', 'modula3': 'Modula3', 'autoit': 'AutoIt',
        'mpasm': 'MPASM', 'inno': 'InnoScript', 'lotusformulas': 'LotusFormulas',
        'locobasic': 'LocoBasic', 'whitespace': 'WhiteSpace', 'scala': 'Scala',
        'xpp': 'XPP', 'applescript': 'AppleScript', 'per': 'Per', 'lua': 'Lua',
        'verilog': 'VeriLog', 'qbasic': 'QBasic', 'progress': 'Progress',
        'email': 'Email', 'bf': 'BrainFuck', 'asp': 'ASP',
        'visualprolog': 'VisualProLog', 'ocaml-brief': 'OCalmBrief',
        'vala': 'Vala', 'javascript': 'JavaScript', 'newlisp': 'newLISP',
        'robots': 'Robots', 'caddcl': 'CADDCL', 'mapbasic': 'MapBasic',
        'html5': 'HTML5', 'hicest': 'HicEst', 'apache': 'ApacheLog',
        'dcs': 'DCS', 'algol68': 'ALGOL68', 'pike': 'Pike', 'c': 'C',
        'postgresql': 'PostgreSQL', 'winbatch': 'WinBatch', 'ocaml': 'OCaml',
        'm68k': 'M68000Assembler', 'idl': 'IDL', 'oz': 'Oz',
        'objc': 'ObjectiveC', 'boo': 'BOO', 'objeck': 'ObjeckProgrammingLangua',
        'clojure': 'Clojure', 'chaiscript': 'ChaiScript',
        'xorg_conf': 'XorgConfig', 'uscript': 'UnrealScript',
        'glsl': 'OpenGLShading', 'bascomavr': 'BASCOMAVR',
        'autohotkey': 'Autohotkey', 'cadlisp': 'CADLisp',
        'proftpd': 'ProFTPd', 'cuesheet': 'Cuesheet', 'sql': 'SQL',
        'smarty': 'Smarty', 'vim': 'VIM', 'haskell': 'Haskell',
        'diff': 'Diff', 'pycon': 'PyCon', 'pcre': 'PCRE',
        'html4strict': 'HTML', 'properties': 'Properties',
        'java': 'Java', 'yaml': 'YAML', 'teraterm': 'TeraTerm',
        'rails': 'Rails', 'perl': 'Perl', 'oobas': 'OpenofficeBASIC',
        'pascal': 'Pascal', 'rebol': 'REBOL', 'pf': 'OpenBSDPACKETFILTER',
        'bash': 'Bash', 'povray': 'POV-Ray', 'thinbasic': 'thinBasic',
        'fo': 'FOLanguage', 'oxygene': 'DelphiPrism(Oxygene)',
        'sdlbasic': 'SdlBasic', 'oracle8': 'Oracle8',
        '68000devpac': 'Motorola68000HiSoftDev', 'mirc': 'mIRC',
        'java5': 'Java5', 'tcl': 'TCL', 'ruby': 'Ruby',
        'cpp-qt': 'C++(withQTextensions)', 'groovy': 'Groovy',
        'scheme': 'Scheme', 'modula2': 'Modula2', 'vbnet': 'VB.NET',
        'oracle11': 'Oracle11', 'j': 'J', 'typoscript': 'TypoScript',
        'cil': 'CIntermediateLanguage', 'magiksf': 'MagikSF',
        'autoconf': 'autoconf', 'powershell': 'PowerShell', 'prolog': 'Prolog',
        'f1': 'FormulaOne', 'vb': 'VisualBasic', 'pawn': 'PAWN',
        'mxml': 'MXML', 'cobol': 'COBOL', 'ini': 'INIfile', 'io': 'IO',
        'sas': 'SAS', 'smalltalk': 'Smalltalk', 'rpmspec': 'RPMSpec',
        'asm': 'ASM(NASM)', 'blitzbasic': 'BlitzBasic', 'cmake': 'CMake',
        'apt_sources': 'APTSources', 'gnuplot': 'RubyGnuplot',
        'basic4gl': 'Basic4GL', 'make': 'Make', 'lotusscript': 'LotusScript',
        'avisynth': 'Avisynth', 'lscript': 'LScript', 'gettext': 'GetText',
        'coffeescript': 'CoffeeScript', 'delphi': 'Delphi',
        'actionscript': 'ActionScript', 'cfdg': 'CFDG', 'css': 'CSS',
        '6502kickass': '6502KickAssembler', 'oberon2': 'Oberon2',
        'llvm': 'LLVM', 'powerbuilder': 'PowerBuilder', 'whois': 'WHOIS',
        'eiffel': 'Eiffel', '4cs': '4CS', 'actionscript3': 'ActionScript3',
        'visualfoxpro': 'VisualFoxPro', 'awk': 'Awk', 'dos': 'DOS',
        'intercal': 'INTERCAL', 'php': 'PHP', 'tsql': 'T-SQL', 'icon': 'Icon',
        'latex': 'Latex', 'e': 'E', 'klonecpp': 'CloneC++', 'q': 'q/kdb+',
        'nsis': 'NullSoftInstaller', 'logtalk': 'Logtalk', 'bibtex': 'BibTeX',
        'ecmascript': 'ECMAScript', 'cpp': 'C++', 'genie': 'Genie',
        'scilab': 'Scilab', 'epc': 'EPC', 'dot': 'DOT'
    }

    def get_api_user_key(self, api_dev_key, username=None, password=None):
        '''
        Get api user key to enable posts from user accounts if username
        and password available.
        Not getting an api_user_key means that the posts will be "guest" posts
        '''
        username = username or get_config('pastebin', 'api_user_name')
        password = password or get_config('pastebin', 'api_user_password')
        if username and password: 
            data = {
                'api_user_name': username,
                'api_user_password': password,
                'api_dev_key': api_dev_key,
            }
            urlencoded_data = urllib.urlencode(data)
            req = urllib2.Request('http://pastebin.com/api/api_login.php',
                                  urlencoded_data)
            response = urllib2.urlopen(req)
            user_key = response.read()
            logging.debug("User key: %s" % user_key)
            return user_key
        else:
            logging.info("Pastebin: not using any user key")
            return ""

    def process_response(self):
        resp = self.response.read()
        if "Bad API request" in resp:
            raise PasteException("Error while submitting paste: %s" % resp)
        elif len(resp) == 0:
            raise PasteException("Pastebin did not return any data")
        else:
            return resp

    def process_data(self):
        self.data['api_paste_format'] = self.data['syntax'] or 'text'
        self.data['api_paste_code'] = self.data['content']
        self.data['api_paste_name'] = self.data['title']
        if self.data['poster']:
            self.data['api_paste_name'] += ' ' if self.data['title'] else ''
            self.data['api_paste_name'] += 'by %s' %(self.data['poster'])
        self.data['api_option'] = 'paste'
        self.data['api_paste_private'] = 1 if self.data['private'] else 0
        # Expiry date according to `hold` flag and `api_paste_expire_date`
        # config
        if self.data['hold']:
            self.data['api_paste_expire_date'] = 'N'
        else:
            self.data['api_paste_expire_date'] = get_config('pastebin',
                                                            'api_paste_expire_date',
                                                            False,
                                                            '1M')
        
        # api_dev_key supplied as an option?
        if "api_dev_key" not in self.data or self.data['api_dev_key'] is None:
            logging.debug("Reading api_dev_key from config")
            self.data['api_dev_key'] = get_config('pastebin', 'api_dev_key', allow_empty_option=False)

        assert self.data['api_dev_key'] is not None and len(self.data['api_dev_key']) > 0
        logging.debug("Using %s as api_dev_key" % self.data['api_dev_key'])
        #Get the pastebin user key
        self.data['api_user_key'] = self.get_api_user_key(self.data['api_dev_key'])
        return self.data


register_service('dpaste', Dpaste)
register_service('pastebin', PastebinPaste)

# The following functions perform the various listing tasks
# Accessed through paster list <type>
def list_services(data):
    for key in SERVICES.keys():
        logging.info('\t%s%s' %(key, '*' if key==data['service'] else ''))

def list_syntax(data):
    service = get_service(data)
    service.list_syntax()

def list_configs(data):    
    for key in sorted(DEFAULTS.keys()):
        logging.info('\t%s: %s' %(key, DEFAULTS[key]))
        
LISTS = {
    'services': list_services,
    'syntax': list_syntax,
    'configs': list_configs,
}

def list_details(data):
    #Called for sub-method `list`
    list_type = data['type'][0]
    LISTS[list_type](data)
