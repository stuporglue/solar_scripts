#!/usr/bin/env python


import glob,dbconn
from config import *

out_path = config.get('paths','solar_raster_output_dir')

print "Checking files in " + out_path

# Reset everything
q = "UPDATE sa_fishnets SET state=0"
dbconn.run_query(q)

for dirname in glob.glob(out_path + "\\*"):
    print "Processing " + dirname
    updatewhere = []
    for img in glob.glob(dirname + '\\*.img'):
        updatewhere.append(img.replace(dirname + '\\SRR_','').replace('.img',''))

    if len(updatewhere) > 0:
        print "Updating " + str(len(updatewhere))
        q = "UPDATE sa_fishnets SET state=2 WHERE state<>2 AND id IN (" + ','.join(updatewhere) + ")"
        dbconn.run_query(q)


q = "SELECT id FROM sa_fishnets"
res = dbconn.run_query(q)
ids = []
for row in res:
    ids.append(row['id'])

print "Still missing " . ','.join(ids)
