#!/usr/bin/env python


import glob,dbconn
from config import *

out_path = config.get('paths','solar_raster_output_dir')

print "Checking files in " + out_path

for dirname in glob.glob(out_path + "\\*"):
    print "Processing " + dirname
    updatewhere = []
    for img in glob.glob(dirname + '\\*.img'):
        updatewhere.append(img.replace(dirname + '\\SRR_','').replace('.img',''))

    if len(updatewhere) > 0:
        print "Updating " + str(len(updatewhere))
        q = "UPDATE sa_fishnets SET state=2 WHERE state<>2 AND id IN (" + ','.join(updatewhere) + ")"
        dbconn.run_query(q)
