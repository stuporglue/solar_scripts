#!/usr/bin/env python
# -*- coding: utf-8 -*-
from config import *
import os
import glob

outdir = "F:\\Minneasdfasdf"
paths = ["F:\\Minnesotasdfasdfasdf\SRR"]
for path in paths:
    for img in glob.glob(path + '\\*.img'):
        imgnumber = int(img.replace(path,'').replace('SRR_','').replace('.img'))
        dirname = 'SRR_' + str(imgnumber / 1000 * 1000).zfill(4) # Make 3 zeros at the end

        if not os.path.exists(outdir + os.path.sep + dirname):
            os.mkdir(dirname)

        filenames = P
                path + os.path.sep + 'SRR_' + imgnumber + '.img' : path + os.path.sep + dirname + os.path.sep + 'SRR_' + imgnumber + '.img',
                path + os.path.sep + 'SRR_' + imgnumber + '.img.aux.xml' : path + os.path.sep + dirname + os.path.sep + 'SRR_' + imgnumber + '.img.aux.xml',
                path + os.path.sep + 'SRR_' + imgnumber + '.img.xml' : path + os.path.sep + dirname + os.path.sep + 'SRR_' + imgnumber + '.img.xml',
                path + os.path.sep + 'SRR_' + imgnumber + '.rrd' : path + os.path.sep + dirname + os.path.sep + 'SRR_' + imgnumber + '.rrd'
                }

        pathexists = False
        for src,dst in filenames.iteritems():
            if not os.path.exists(src):
                print "Trying to copy file that doesn't exist:"
                print img + ' as ' + src

            if os.path.exists(dst):
                pathexists = True

        if not pathexists:
            for src,dst in filenames.iteritems():
                print "Rename " + src + " to " + dst


