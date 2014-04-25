#!/usr/bin/env python
# Test if the database connection is working

try:
    import sys
    from config import *
    from distutils.spawn import find_executable

    print config.get('projection','srid')
    print config.get('solar_analyst','sky_size')


    import dbconn
    
    # Test 2: Do they have PostGIS?
    res = dbconn.run_query("SELECT PostGIS_full_version() AS pg").fetchone()
    if res is None:
        print "It looks like your database doesn't have PostGIS installed"
        raise
    
    # Test 3: How about the specified schema?
    res = dbconn.run_query("SELECT schema_name FROM information_schema.schemata WHERE schema_name = '" + config.get('postgres','schema') + "'").fetchone()
    if res is None:
        print "I couldn't find the specified schema"
        raise
 
 
    for path in config.items('paths'):
        if not os.path.isdir(path[1]):
            print "Path does not exist -- " + ":".join(path)
            raise

    if find_executable('blast2dem') == None:
        print "blast2dem.exe was not found in your PATH"
        raise
    

    if find_executable('lasindex') == None:
        print "lasindex.exe was not found in your PATH"
        raise

    # If we made it this far, we're probably good to go
    print "Everything looks good!"

except:
    # Do nothing, except not crash
    print ""
