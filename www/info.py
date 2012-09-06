#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import sys
import json 
import zlib
import httplib

cgitb.enable()
sys.path.append('../python')

from build_html import editable_castell_plan
import db_interaction

form = cgi.FieldStorage()
what = form["what"].value

db = db_interaction.get_db()

print "Content-Type: application/json"     # HTML is following
print                               # blank line, end of headers

if what=='get_colla':
    colla_id = form["colla_id"].value
#    print json.dumps(db_interaction.get_colla(db, colla_id), separators=(',', ':'))
    res = {'Price':54,'Cost':'99'}
    print json.dumps(res)

else:
    print "Unexpected argument: ", what
