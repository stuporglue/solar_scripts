#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser,os,sys

config = ConfigParser.ConfigParser()

# Read in the defaults
conffile = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'defaults.cfg'
config.readfp(open(conffile))

# Read in the user settings
conffile = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'config.cfg'

if not os.path.isfile(conffile):
    print "The conf file: " + conffile + " is required"
    raise

config.readfp(open(conffile))
os.environ["PATH"] += os.pathsep + config.get('paths','lastools_bin_dir') 

try:
    libs = config.get('paths','extra_python_dirs') 
    sys.path += libs.split(';')
except:
    # Do nothing. Must nut have an extra_python_dirs value
    pass
