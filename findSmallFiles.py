#!/usr/bin/env python

import os
import glob,dbconn
from config import *
import shutil

outdir = "F:\SolarResourceData\Final_SRR_Rerun"

os.chdir('F:\\SolarResourceData\\Final_SRR\\')

out_path = "F:\SolarResourceData\Final_SRR"

#out_path = config.get('paths','solar_raster_output_dir')
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
        if os.path.getsize(img) <= 2048231:
            imgnumber = img.replace(dirname + '\\SRR_','').replace('.img','')
            updatewhere.append(imgnumber)
            for ext in extensions:
                srcfile = out_path + "\\" + dirno + "\\SRR_" + imgnumber + ext
                dstfile = subdir + "\\SRR_" + imgnumber + ext
                try:
                    shutil.move(srcfile,dstfile)
                except:
                    pass


    if len(updatewhere) > 0:
        print updatewhere
        #exit()
    print "Updating " + str(len(updatewhere))
    q = "UPDATE sa_fishnets SET state=0 WHERE state<>0 AND id IN (" + ','.join(updatewhere) + ")"
    dbconn.run_query(q)
