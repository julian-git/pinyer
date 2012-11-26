#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import sys
import json 
import zlib
import httplib
import pickle

cgitb.enable()
sys.path.append('../python')

from local_config import RootDir, pinya_dir
sys.path.append(RootDir + 'python/util/')
from build_html import solution_as_svg
from solve_ip import solve_castell
from db_interaction import get_db, db_nicknames_and_char, db_casteller_presence


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
    colla_id_name = form["colla_id_name"].value
    char = sanitize(form, "char", 
                    ['total_height', 'shoulder_height', \
                         'axle_height', 'hip_height', 'stretched_height', \
                         'shoulder_height', 'shoulder_width'])
    colla = db_nicknames_and_char(db, colla_id_name, char)
    print json.dumps(colla, separators=(',', ':'), ensure_ascii=False)

elif what=='absent_castellers':
    colla_id_name = form["colla_id_name"].value
    absent_castellers = db_casteller_presence(db, colla_id_name, 0)
    print json.dumps(absent_castellers, separators=(',', ':'), ensure_ascii=False)    

elif what=='idle_castellers':
    colla_id_name = form["colla_id_name"].value
    castell_id_name = form["castell_id_name"].value
    filename = RootDir + '/www/' + pinya_dir + '/' + castell_id_name + '/pinya'
    f = open(filename + '.active_castellers', 'r')
    active_castellers = pickle.load(f)
    present_castellers = db_casteller_presence(db, colla_id_name, 1)
    idle_castellers = sorted(set(present_castellers) - set(active_castellers))
    print json.dumps(idle_castellers, separators=(',', ':'), ensure_ascii=False)

elif what=='solved_pinya':
    castell_id_name = form['castell_id_name'].value
    filename = RootDir + '/www/' + pinya_dir + '/' + castell_id_name + '/pinya'
    f = open(filename + '.solved.svg', 'r')
    print f.read()

elif what=='optimize_pinya':
    prescribed = dict()
    castell_id_name = form['castell_id_name'].value
#
    colla_id_name = 'cvg' # for "real"
#
    solution = solve_castell(prescribed, castell_id_name, colla_id_name)
    positions = [[pos,c['nickname']] for [pos, c] in solution['positions'].iteritems()]
    relations = solution['relations']
    sol_dict = dict([('positions', positions), ('relations', relations)])
    print json.dumps(sol_dict, separators=(',', ':'), ensure_ascii=False)

elif what=='rel_types':
    castell_id_name = form['castell_id_name'].value
#
    colla_id_name = 'cvg' # for "real"
#
    filename =  RootDir + '/www/' + pinya_dir + '/' + castell_id_name + '/pinya' 
    f2 = open(filename + '.ineq_reps', 'r')
    ineq_reps = dict(pickle.load(f2))
    print json.dumps(ineq_reps, separators=(',', ':'), ensure_ascii=False)

else:
    print "Unexpected argument: ", what
