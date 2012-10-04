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

from build_html import solution_as_svg
from build_ip import solve_castell
from db_interaction import get_db, get_nicknames_and_char
from xml_to_svg import xml_to_svg

form = cgi.FieldStorage()
what = form["what"].value

db = get_db()

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
    colla = get_nicknames_and_char(db, colla_id, char)
    print json.dumps(colla, separators=(',', ':'), ensure_ascii=False)

elif what=='get_pinya':
    pinya_id = form["castell_type_id"].value
    # FIXME the next line must be generalized
    print xml_to_svg('tresde8f.pinya.xml')

elif what=='optimize_pinya':
    prescribed = dict()
    castell_type_id = form["castell_type_id"].value
    colla_id = 1
#
    [castell_type_id, colla_id] = [1000, 2]  # for debugging
#    [castell_type_id, colla_id] = [3, 1] # for "real"
#
    solution = solve_castell(prescribed, castell_type_id, colla_id)
    positions = [[pos,c['nickname']] for [pos, c] in solution['positions'].iteritems()]
    relations = solution['relations']
    sol_dict = dict([('positions', positions), ('relations', relations)])
    print json.dumps(sol_dict, separators=(',', ':'), ensure_ascii=False)

else:
    print "Unexpected argument: ", what
