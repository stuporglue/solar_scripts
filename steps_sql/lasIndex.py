# lasIndex.py
# blast all MN Lidar to DEM
# walz0053@umn.edu
#

import sys, os, subprocess, glob
from distutils.spawn import *

################ Usage check and argument assigning
if len(sys.argv) != 2:
    print "Usage: lasIndex.py <input directory>"
    print "The intput directory should have the q**** directories in it, eg. c:\base\path\to\q***"
    exit(-1)
else:
    basepath = sys.argv[1]

if find_executable('lasindex') == None:
    print "Please make sure that lasindex.exe is in your PATH environment"
    exit(-1)

if not os.path.isdir(basepath):
    print "Input directory must be a directory and exist"
    exit(-1)

################ Running our functions on input data
for curdir in glob.glob(basepath + '\\q*'):
    lazfiles = glob.glob(curdir + '\\laz\\*.laz')
    process = subprocess.Popen("lazindex.exe \\laz\\*.laz -cores 8", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
