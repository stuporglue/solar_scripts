# lasIndex.py
# blast all MN Lidar to DEM
# walz0053@umn.edu
#

import sys, os, subprocess, glob, ConfigParser, re
from distutils.spawn import *

config = ConfigParser.ConfigParser()
conffile = os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'config.cfg'
config.readfp(open(conffile))

basepath = config.get('paths','lasDir')

os.environ["PATH"] += os.pathsep + config.get('paths','lastools_bin_dir') 

if find_executable('lasindex') == None:
    print "Please make sure that lasindex.exe is in your PATH environment"
    exit(-1)

if not os.path.isdir(basepath):
    print "Input directory must be a directory and exist"
    exit(-1)

################ Running our functions on input data
# Walk the directory and handle media files
lasOrLaz = re.compile("(las|laz)$")
for (root, subFolders, files) in os.walk(basepath):
    for onelasfile in files:
        if lasOrLaz.match(onelasfile):
            process = subprocess.Popen("lazindex.exe \\laz\\*.laz -cores " + config.get('data','cores'), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
