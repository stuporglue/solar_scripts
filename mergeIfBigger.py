#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import *
import os
import sys
import glob
import shutil

outdir = "F:\\SolarResourceData\\Final_SRR"
#inputdir = "F:\\SolarResourceData\\Output_SRR_Smallfiles"
#inputdir = "F:\\SolarResourceData\\trash\\Output_SRR_with_folders"
inputdir = "F:\\SolarResourceData\\trash\\Output_SRR_Smallfiles"

for path in glob.glob(inputdir + "\\*"):
    print "Processing " + path
    path += "\\"
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

        print srcbase + '.img'
        print os.path.getsize(srcbase + '.img') 
        print dstbase + '.img'
        print os.path.getsize(dstbase + '.img')
        exit()


        if not os.path.isfile(dstbase + '.img'):
            print "Copying " + srcbase + ".img because it doesn't exist"
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
            print "Copying " + srcbase + ".img because it's bigger"
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
