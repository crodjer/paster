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

string  = '''Python=Python
PythonConsole=Python Interactive/Traceback
Sql=SQL
DjangoTemplate=Django Template/HTML
JScript=JavaScript
Css=CSS
Xml=XML
Diff=Diff
Ruby=Ruby
Rhtml=Ruby HTML (ERB)
Haskell=Haskell
Apache=Apache Config
Bash=Bash script'''

syntax_list = string.split('\n')
print syntax_list

syntax_dict = {}

for syntax in syntax_list:
    syntax=syntax.split('=')
    print syntax
    syntax_dict[syntax[0]]=syntax[1]

print syntax_dict
