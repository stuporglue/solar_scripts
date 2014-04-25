#!/usr/bin/env python
# Test if the database connection is working

import dbconn

res = dbconn.run_query("SELECT PostGIS_full_version() AS pg").fetchall()

print str(res)


# TODO -- Import config file, check that all paths and required arguments exist 

if find_executable('blast2dem') == None:
    print "Please make sure that blast2dem.exe is in your PATH environment"
    exit(-1)

if not os.path.isdir(basepath):
    print "Input directory must be a directory and exist"
    exit(-1)


TODO: 
Test that db has postgis enabled

