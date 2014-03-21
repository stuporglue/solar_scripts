#!/usr/bin/env python

import sys
sys.path.insert(0, '../../../steps_sql') # Add our steps_sql dir to our library path
import dbconn

dbconn.send_query("SELECT id,state,ST_AsGeoJSON(ST_Transform(the_geom,4326)) AS the_geom FROM dem_fishnets")
