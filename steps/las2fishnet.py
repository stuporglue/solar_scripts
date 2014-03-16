#
# blast2dem.py
# blast all MN Lidar to DEM
# walz0053@umn.edu
#

import sys, os, subprocess, glob, re, math
from subprocess import call
from distutils.spawn import *


################ Usage check and argument assigning
if len(sys.argv) != 5:
    print "Usage: las2fishnet.py <input directory> <round digits> <fishnetsize> <output fishnet file>"
    print "The intput directory should have the q**** directories in it, eg. c:\\base\\path\\to\\q***"
    exit(-1)
else:
    basepath     = sys.argv[1]
    roundingsize = 10 ** int(sys.argv[2])
    fishnetsize  = int(sys.argv[3])
    outputfile   = sys.argv[4]

if find_executable('blast2dem') == None:
    print "Please make sure that blast2dem.exe is in your PATH environment"
    exit(-1)

if not os.path.isdir(basepath):
    print "Input directory must be a directory and exist"
    exit(-1)

################ Running our functions on input data
globs = []
for curdir in glob.glob(basepath + '\\q*'):
    globs.append(curdir + '\\laz\\*.laz')


# Check output
command = "lasinfo.exe -i " + " ".join(globs) + " -merged -no_check"
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
output,error = process.communicate()
returncode = process.poll()

if error != None:
    print error
if returncode != 0:
    print output

if error != None or returncode != 0:
    exit(-1)


minline = re.compile('\s*min x y z:\s*(.*)\s+(.*)\s+.*')
maxline = re.compile('\s*max x y z:\s*(.*)\s+(.*)\s+.*')

# String min/max
sminx = smaxx = sminy = smaxy = 0
for line in output.split("\n"):
    matches = minline.match(line.strip())
    if matches:
        sminx = matches.group(1)
        sminy = matches.group(2)
    matches = maxline.match(line.strip())
    if matches:
        smaxx = matches.group(1)
        smaxy = matches.group(2)

# Calculate rounded numbers

# Int minmax
minx = int(float(sminx)) 
maxx = int(float(smaxx)) 
miny = int(float(sminy)) 
maxy = int(float(smaxy)) 

# rounded minmax
rminx = minx / roundingsize * roundingsize
rmaxx = maxx / roundingsize * roundingsize + roundingsize
rminy = miny / roundingsize * roundingsize
rmaxy = maxy / roundingsize * roundingsize + roundingsize

# print "---------------"
# print "String min/max"
# print sminx
# print smaxx
# print sminy
# print smaxy
# print "---------------"
# print "Int min/max"
# print minx
# print maxx
# print miny
# print maxy
# print "---------------"
# print "Rounded min/max"
# print rminx
# print rmaxx
# print rminy
# print rmaxy
# print "---------------"
#  
# print "Bounding box: (" + str(minx) + ',' + str(miny) + '),(' + str(maxx) + ',' + str(maxy) + ')'
print "Bounding box: (" + str(rminx) + ',' + str(rminy) + '),(' + str(rmaxx) + ',' + str(rmaxy) + ')'
# 
# # print the fishnet
# # print "minx,miny,maxx,maxy"
# print roundingsize
# 
# print range(rminx,rmaxx,fishnetsize)

f = open(outputfile,'w')
f.write("xmin,ymin,xmax,ymax" + "\n")
for x in range(rminx,rmaxx,fishnetsize):
    for y in range(rminy,rmaxy,fishnetsize):
        f.write(str(x) + ',' + str(y) + ',' + str(x + fishnetsize) + ',' + str(y + fishnetsize) + "\n")
f.close()
