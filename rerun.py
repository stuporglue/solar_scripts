#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Test if the database connection is working

import sys
from config import *
from distutils.spawn import find_executable
import dbconn

rr = "180697"
q = "UPDATE sa_fishnets SET state=0 WHERE state<>0 AND id IN (" + rr + ")"
dbconn.run_query(q)
