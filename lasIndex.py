# lasIndex.py
# blast all MN Lidar to DEM
# walz0053@umn.edu
#

import os, subprocess, re
from distutils.spawn import find_executable
from config import *

basepath = config.get('paths','las_dir')

################ Running our functions on input data
# Walk the directory and handle media files
lasOrLaz = re.compile(".*(las|laz)$")
print "Walking " + basepath
for (root, subFolders, files) in os.walk(basepath):
    for onelasfile in files:
        if lasOrLaz.match(onelasfile):
            fullname = root + os.path.sep + onelasfile

            # Only make index if it's not already there
            if not os.path.isfile(fullname.replace('.laz','.lax').replace('.las','.lax')):
                command = find_executable("lasindex.exe") + " -i " + fullname + " -cores " + config.get('processing','cores')
                subprocess.call(command)
