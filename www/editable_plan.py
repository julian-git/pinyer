#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi
import cgitb
import sys

cgitb.enable()
sys.path.append('..')

from build_html import editable_castell_plan

form = cgi.FieldStorage()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers
print editable_castell_plan(form["castell_id"].value)
