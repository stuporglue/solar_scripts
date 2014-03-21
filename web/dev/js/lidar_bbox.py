#!/usr/bin/env python

import sys,os

sys.path.insert(0, '../../../steps_sql') # Add our steps_sql dir to our library path
import dbconn

if os.path.isfile('lidar_bbox.json'):
    print "Content-Type: application/json; charset=utf-8"
    print
    with open('lidar_bbox.json', 'r') as fin:
        print fin.read()
    exit()

js = dbconn.send_query("SELECT id,lasfile,ST_AsGeoJSON(ST_Transform(the_geom,4326)) AS the_geom FROM lidar_bbox")

f = open('lidar_bbox.json', 'w')
f.write(js)
f.close()
