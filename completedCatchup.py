#!/usr/bin/env python


import glob,dbconn
from config import *

out_path = config.get('paths','solar_raster_output_dir')

updatewhere = []

max = 1000

for img in glob.glob(out_path + '\\*.img'):
    updatewhere.append(img.replace(out_path + '\\SRR_','').replace('.img',''))

    if len(updatewhere) > max:
        q = "UPDATE sa_fishnets SET state=2 WHERE state<>2 AND id IN (" + ','.join(updatewhere) + ")"
        dbconn.run_query(q)

if len(updatewhere) > 0:
    q = "UPDATE sa_fishnets SET state=2 WHERE state<>2 AND id IN (" + ','.join(updatewhere) + ")"
    dbconn.run_query(q)
