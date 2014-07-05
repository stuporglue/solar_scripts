#!/usr/bin/env python

import os
import glob,dbconn
from config import *
import shutil
import datetime

outdir = "F:\SolarResourceData\Final_SRR_From_USpatial"

os.chdir('F:\\SolarResourceData\\Final_SRR\\')

out_path = config.get('paths','solar_raster_output_dir')
print "Checking files in " + out_path

extensions = [
        '.img',
        '.img.aux.xml',
        '.rrd',
        '.img.xml'
        ]

for dirname in glob.glob(out_path + "\\*"):
    print "Processing " + dirname

    dirno = dirname.replace(out_path,'')
    subdir = outdir + dirno
    if not os.path.exists(subdir):
        os.mkdir(subdir)


    updatewhere = []
    for img in glob.glob(dirname + '\\*.img'):
        ctime = os.path.getctime(img)
        if ctime > 1401548400:   # 5/31/2014 @ 15:0:0 UTC
            print datetime.datetime.fromtimestamp(ctime)
            imgnumber = img.replace(dirname + '\\SRR_','').replace('.img','')
            updatewhere.append(imgnumber)
            for ext in extensions:
                srcfile = out_path + "\\" + dirno + "\\SRR_" + imgnumber + ext
                dstfile = subdir + "\\SRR_" + imgnumber + ext
                try:
                    shutil.copy2(srcfile,dstfile)
                except:
                    pass
#
#
#    if len(updatewhere) > 0:
#        print updatewhere
#        #exit()
#    print "Updating " + str(len(updatewhere))
#    q = "UPDATE sa_fishnets SET state=0 WHERE state<>0 AND id IN (" + ','.join(updatewhere) + ")"
#    dbconn.run_query(q)
