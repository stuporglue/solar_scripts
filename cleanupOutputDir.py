#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import *
import os
import sys
import glob
import shutil

outdir = "F:\SolarResourceData\Final_SRR"

paths = ["F:\\SolarResourceData\\FromMSI\Output_SRR\\"]

for path in paths:
    print "Processing " + path
    for img in glob.glob(path + '\\*.img'):
        imgnumber = int(img.replace(path,'').replace('SRR_','').replace('.img',''))
        dirname = outdir + os.path.sep + 'SRR_' + str(imgnumber / 1000 * 1000).zfill(4) + os.path.sep # Make 3 zeros at the end

        if not os.path.exists(dirname):
            os.mkdir(dirname)

        srcbase = path + 'SRR_' + str(imgnumber)
        dstbase = dirname + 'SRR_' + str(imgnumber)

        extensions = [
                '.img',
                '.img.aux.xml',
                '.rrd',
                '.img.xml'
                ]


        if not os.path.isfile(dstbase + '.img'):
            print "Copygin " + dstbase + " because it doesn't exist"
            for ext in extensions:
                try:
                    shutil.move(srcbase + ext,dstbase + ext)
                except:
                    try:
                        shutil.copy2(srcbase + ext,dstbase + ext)
                    except:
                        print sys.exc_info()
                        exit()
        elif os.path.getsize(srcbase + '.img') > os.path.getsize(dstbase + '.img'):
            print "Copygin " + dstbase + " because it's bigger"
            for ext in extensions:
                try:
                    shutil.move(srcbase + ext,dstbase + ext)
                except:
                    try:
                        shutil.copy2(srcbase + ext,dstbase + ext)
                    except:
                        print sys.exc_info()
                        exit()
        else:
            pass
