#!/usr/bin/env python
# -*- coding: utf-8 -*-

# lasIndex.py
# blast all MN Lidar to DEM
# walz0053@umn.edu
#

import sys, os, subprocess, glob, re
from distutils.spawn import *
from config import *

basepath = config.get('paths','lasDir')

################ Running our functions on input data
# Walk the directory and handle media files
lasOrLaz = re.compile("(las|laz)$")
for (root, subFolders, files) in os.walk(basepath):
    for onelasfile in files:
        if lasOrLaz.match(onelasfile):
            process = subprocess.Popen("lazindex.exe \\laz\\*.laz -cores " + config.get('data','cores'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            output,error = process.communicate()
            returncode = process.poll()
