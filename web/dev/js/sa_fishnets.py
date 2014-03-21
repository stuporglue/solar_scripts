#!/usr/bin/env python

import sys
sys.path.insert(0, '../../../steps_sql') # Add our steps_sql dir to our library path
import dbconn

#!/usr/bin/env python

import sys,os

sys.path.insert(0, '../../../steps_sql') # Add our steps_sql dir to our library path
import dbconn

if os.path.isfile('sa_fishnets.json'):
    print "Content-Type: application/json; charset=utf-8"
    print
    with open('sa_fishnets.json', 'r') as fin:
        print fin.read()
    exit()

js = dbconn.send_query("SELECT id,ST_AsGeoJSON(ST_Transform(the_geom,4326)) AS the_geom FROM sa_fishnets")

f = open('sa_fishnets.json', 'w')
f.write(js)
f.close()
