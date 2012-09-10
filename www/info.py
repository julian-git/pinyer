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

def sanitize(form, arg, whitelist):
    if arg not in form.keys():
        raise Exception("Need argument for ", arg)
    val = form[arg].value
    if val in whitelist:
        return val
    else:
        raise Exception("unexpected argument: ", val)
        


print 'Content-Type: application/json, charset="utf-8"'     # HTML is following
print                               # blank line, end of headers

if what=='get_colla':
    colla_id = form["colla_id"].value
    char = sanitize(form, "char", 
                    ['total_height', 'shoulder_height', \
                         'axle_height', 'hip_height', 'stretched_height', \
                         'shoulder_height', 'shoulder_width'])
    colla = db_interaction.get_nicknames_and_char(db, colla_id, char)
    print json.dumps(colla, separators=(',', ':'), ensure_ascii=False)

if what=='get_pinya':
    pinya_id = form["pinya_id"].value
    pinya = db_interaction.get_positions(db, pinya_id)
    print json.dumps(pinya, separators=(',', ':'), ensure_ascii=False)

else:
    print "Unexpected argument: ", what
