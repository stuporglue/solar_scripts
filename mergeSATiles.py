#!/usr/bin/env python

import os,subprocess
import glob,dbconn_quick
import os.path
from config import *
import shutil

sabase = 'F:\\SolarResourceData\\Final_SRR\\'
samergedbase = "F:\\SolarResourceData\\Merged_Final_SRR\\"
gdal_merge = "python.exe D:\\Scripts\\bin\\gdal\\python\\scripts\\gdal_merge.py"

os.environ['GDAL_DRIVER_PATH'] = "D:\\Scripts\\bin\\gdal\\plugins"
os.environ['GDAL_DATA'] = "D:\\Scripts\\bin\\gdal-data"

reserveq = """SELECT id FROM dem_fishnets ORDER BY id"""

satileq = """
SELECT sa.id FROM sa_fishnets sa,dem_fishnets dem WHERE
dem.id=DEMID AND
st_contains(dem.the_geom,sa.the_geom)
"""

cmds = ""

res = dbconn_quick.run_query(reserveq)
rownum = 0
bat = open("merge_sa_tiles.bat","w")

for row in res:
    rownum += 1
    demid = str(row['id'])

    print "On row " + str(rownum) + " (" + demid + ")"

    outputfile = samergedbase + demid + '.img'

    if not os.path.isfile(outputfile):

        satilesres = dbconn_quick.run_query(satileq.replace('DEMID',demid))
        tilepaths = []
        for imgrow in satilesres:
            imgnumber = imgrow['id']
            dirname = sabase + os.path.sep + 'SRR_' + str(imgnumber / 1000 * 1000).zfill(4) + os.path.sep + 'SRR_' + str(imgnumber) + '.img'
            tilepaths.append(dirname)

        if len(tilepaths) > 0:
            cmd = gdal_merge + ' -o ' + outputfile + ' ' + ' '.join(tilepaths) + "\n"
            bat.write(cmd)

bat.close()
