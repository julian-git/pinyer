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

print 'Content-Type: application/json, charset="utf-8"'     # HTML is following
print                               # blank line, end of headers

if what=='get_colla':
    colla_id = form["colla_id"].value
    _char = form["char"].value
    if _char in ['total_height', 'shoulder_height', 'axle_height', 'hip_height', 'stretched_height', 'shoulder_height', 'shoulder_width']:
        char=_char
    else:
        raise Exception("unexpected argument: ", _char)
        
    colla = db_interaction.get_nicknames_and_char(db, colla_id, char)
    print json.dumps(colla, separators=(',', ':'), ensure_ascii=False)

else:
    print "Unexpected argument: ", what
