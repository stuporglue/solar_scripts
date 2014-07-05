#!/usr/bin/env python

import os,subprocess
import glob,dbconn_quick
import os.path
from config import *
import shutil

sourcedir = 'F:\\SolarResourceData\\Final_SRR\\'
destdir = "R:\\SA_Tiles_By_County\\"

county_to_demid = """
SELECT countyname AS county, d.id AS demid FROM county c, dem_fishnets d WHERE ST_INTERSECTS(c.the_geom,d.the_geom) ORDER BY position('Hennepin' IN countyname) DESC 
"""

countyres = dbconn_quick.run_query(county_to_demid)

cur_county = ""
cur_dem = -1
for county in countyres:

    if cur_county != county['county']:
        print "Working on county: " + county['county']
        cur_county = county['county']

    if cur_dem != county['demid']:
        print "\tWorking on DEM tile " + str(county['demid'])
        cur_dem = county['demid']

    try: 
        os.makedirs(destdir + county['county'])
    except OSError as err:
        if err.errno != 17:
            raise

    try:
        os.makedirs(destdir + county['county'] + '\\' + str(county['demid']))
    except OSError as err:
        if err.errno != 17:
            raise

    demid_to_said = """
        SELECT s.id, (s.id/1000*1000) AS dir FROM dem_fishnets d,sa_fishnets s WHERE ST_INTERSECTS(d.the_geom,s.the_geom) AND d.id=""" + str(county['demid']) + """
    """

    satileres = dbconn_quick.run_query(demid_to_said)

    for satile in satileres:
        print "\t\t" + str(satile['id']) + '.img'
        if not os.path.isfile(destdir + county['county'] + '\\' + str(county['demid']) + '\\' + str(satile['id']) + '.img'):
            try: 
                shutil.copy2(sourcedir + 'SRR_' + str(satile['dir']) + '\\SRR_' + str(satile['id']) + '.img', destdir + county['county'] + '\\' + str(county['demid']) + '\\' + str(satile['id']) + '.img')
            except: 
                print "Unable to copy file: " + sourcedir + 'SRR_' + str(satile['dir']) + '\\SRR_' + str(satile['id']) + '.img'

        


