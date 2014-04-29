#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Test if the database connection is working

from config import *

print config.get('projection','srid')
print config.get('solar_analyst','sky_size')



#config = ConfigParser.ConfigParser()
#conffile = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'config.cfg'
#
## Test 1: Conf file exists 
#if not os.path.isfile(conffile):
#    print "Cannot find config file " + conffile
#    exit()
#
#config.readfp(open(conffile))

# import dbconn
# 
# # Test 2: Do they have PostGIS?
# res = dbconn.run_query("SELECT PostGIS_full_version() AS pg").fetchall()
# 
# # Test 3: How about the specified schema?
# res = dbconn.run_query("SELECT schema_name FROM information_schema.schemata WHERE schema_name = " + config.get('postgres','schema'))
# 
# 
# # TODO -- Import config file, check that all paths and required arguments exist 
# 
# for path in config.items('paths'):
#     if not os.path.isdir(path[1]):
#         print "Path does not exist -- " + ":".join(path)
#         exit()
# 
# if find_executable('blast2dem') == None:
#     print "Please make sure that blast2dem.exe is in your PATH environment"
#     exit(-1)
# 
# if not os.path.isdir(basepath):
#     print "Input directory must be a directory and exist"
#     exit(-1)
# 
# 
# TODO: 
# Test that db has postgis enabled
# 

#if find_executable('lasindex') == None:
#    print "Please make sure that lasindex.exe is in your PATH environment"
#    exit(-1)
#
#if not os.path.isdir(basepath):
#    print "Input directory must be a directory and exist"
#    exit(-1)


