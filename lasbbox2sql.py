#!/usr/bin/env python
# -*- coding: utf-8 -*-

# For every las file, get its bounding box and insert it into Database
# This could easily be adapter to any other SQL server
# 
# Note that the_geom is in EPSG:4326
# DB structure: the_geom (polygon),lasfile (varchar),processed (bool)

import sys,os,re,math,glob,subprocess,dbconn
from subprocess import call
from distutils.spawn import *
from config import *

os.environ["PATH"] += os.pathsep + config.get('paths','lastools_bin_dir') 

datasrid = config.get('data','srid')
maxinserts = int(config.get('postgres','maxinserts'))
tablename = config.get('postgres','lidar_bbox_table')

basepath     = config.get('paths','lasDir')

minline = re.compile('\s*min x y z:\s*(.*)\s+(.*)\s+.*')
maxline = re.compile('\s*max x y z:\s*(.*)\s+(.*)\s+.*')

################ Insert an array into Database
def insertIntoDatabase(tablerows):
    queryprefix = "INSERT INTO " + config.get('postgres','schema') + "."  + tablename + " (lasfile,the_geom) VALUES "
    query = queryprefix + ",".join(tablerows) + ";\n"
    return dbconn.run_query(query)

################ Running our functions on input data
# Max and Floor coordinates to the nearest int outwards

tablerows = []
sql = ""

for (root, subFolders, files) in os.walk(basepath):
    for lazfile in files:
        command = "lasinfo.exe -i " + lazfile + " -merged -no_check"
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        output,error = process.communicate()
        returncode = process.poll()

        if error != None:
            print error 
        if returncode != 0:
            print output

        sminx = smaxx = sminy = smaxy = 0
        for line in output.split("\n"):
            matches = minline.match(line.strip())
            if matches:
                # Round/buffer outward so we are sure to include everything
                sminx = str(int(math.floor(float(matches.group(1)))))
                sminy = str(int(math.floor(float(matches.group(2)))))
            matches = maxline.match(line.strip())
            if matches:
                smaxx = str(int(math.ceil(float(matches.group(1)))))
                smaxy = str(int(math.ceil(float(matches.group(2)))))

        tablerows.append("('" + lazfile.replace(basepath,'') + "',"+ "ST_MakeEnvelope(" + sminx + "," + sminy + "," + smaxx + "," + smaxy + "," + str(datasrid) + "))")

        if len(tablerows) >= maxinserts:
            insertIntoDatabase(tablerows)
            tablerows = []

if len(tablerows) > 0:
    insertIntoDatabase(tablerows)

print "Done"
