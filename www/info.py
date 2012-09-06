#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import sys

cgitb.enable()
sys.path.append('../python')
sys.path.append('sql')

from build_html import editable_castell_plan
from sql_castellers import get_colla

form = cgi.FieldStorage()
what = form["what"].value

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

if what=='colla':
    print get_colla(form["colla_id"].value)

else:
    print "Unexpected argument: ", what
