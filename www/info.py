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

from create_pinya import tresde8f
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

elif what=='get_pinya':
    pinya_id = form["pinya_id"].value
    [svg, position_at, relations] = tresde8f()
    print svg

elif what=='optimize_pinya':
    prescribed = dict()
    position_data = get_positions(db, castell_type_id)
    castell_type_id = 3
    colla_id = 1
    print find_pinya(prescribed, position_data, castell_type_id, colla_id)

else:
    print "Unexpected argument: ", what
