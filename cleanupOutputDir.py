#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import *
import os
import sys
import glob
import shutil

outdir = "F:\SolarResourceData\Final_SRR"

paths = ["F:\\SolarResourceData\\Output_SRR\\",
         "F:\\SolarResourceData\\FromMSI\Output_SRR\\",
         "F:\\SolarResourceData\\Output_SRR_From_fileshare\\Output_SRR\\"
         ]
for path in paths:
    print "Processing " + path
    for img in glob.glob(path + '\\*.img'):
        imgnumber = int(img.replace(path,'').replace('SRR_','').replace('.img',''))
        dirname = outdir + os.path.sep + 'SRR_' + str(imgnumber / 1000 * 1000).zfill(4) + os.path.sep # Make 3 zeros at the end

        if not os.path.exists(dirname):
            os.mkdir(dirname)

        filenames = {
                path + 'SRR_' + str(imgnumber) + '.img.aux.xml' : dirname + 'SRR_' + str(imgnumber) + '.img.aux.xml',
                path + 'SRR_' + str(imgnumber) + '.img.xml' : dirname + 'SRR_' + str(imgnumber) + '.img.xml',
                path + 'SRR_' + str(imgnumber) + '.rrd' : dirname + 'SRR_' + str(imgnumber) + '.rrd',
                path + 'SRR_' + str(imgnumber) + '.img' : dirname + 'SRR_' + str(imgnumber) + '.img'
                }

        #print img

        for src,dst in filenames.iteritems():
            if os.path.isfile(src):
                #print "Src file " + src + " found (good)"
                if not os.path.isfile(dst):
                    #print "Dest file " + dst + " not found (good)"
                    print "Moving " + src + " to " + dst
                    #sys.stdout.write('.')
                    try:
                        shutil.move(src,dst)
                    except:
                        try:
                            shutil.copy2(src,dst)
                        except:
                            print sys.exc_info()
                            exit()
                else:
                    print dst + " already exists"

        #exit()


