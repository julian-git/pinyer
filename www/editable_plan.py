#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
from build_html import editable_castell_plan

print 'Content-type: text-plain'
print editable_castell_plan(1)
