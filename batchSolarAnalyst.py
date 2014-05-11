#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ---------------------------------------------------------------------------
# batchSolarAnalyst.py
# Created on: 2014-16-08 
# Description: Generate solar radiation tiles for all areas in a shapefile
# ---------------------------------------------------------------------------

# Calculate solar radiation over a very large area by using a Raster Dataset as the source
# and using a database with a fishnet of polygons to choose which areas to use as extents.
# 
# Also takes a buffer size which will be applied to each polygon for use in the extent so that
# output rasters will have edges that match

# The final image output will be clipped back to the size of the input polygon


# Pseudo Code!
# For eachPolygon in fishnet where state is 0:
#   bufferedPollygon = buffer polygon by bufferAmount
#   set extent env to bufferedPolygon
#   outputRaster = AreaSolarRadiation(rasterDataset)
#   clippedOutput = clip outputRaster back to polygon size
#   write clippedOutput file to designated directory

print "Importing libraries"
import sys,os,time,dbconn_quick,tempfile,shutil,datetime
print "Importing config"
from config import *
print "Importing arcpy"
import arcpy
print "Ready to go"

# Define workspace and input datasets
ws = config.get('paths','workspace')
in_surface_raster = config.get('paths','dem_mosaic')
out_path = config.get('paths','solar_raster_output_dir')


# Check out spatial analyst and set ArcGIS environment settings
print "Checking out the spatial extension"
arcpy.CheckOutExtension("spatial")

print "Making temp paths"
workspace = tempfile.mkdtemp(prefix='results_',dir=config.get('paths','temp_dir'))
if not os.path.isdir(workspace):
    print "ERROR! Couldn't create workspace directory " + workspace
    exit()

arcpy.env.workspace = workspace

print "Making scratch workspace"
# Make a temp directory to avoid the FATAL ERROR (INFADI)  MISSING DIRECTORY error 
# NOTE: Delete this later (last line of script)
# Seems like dir should be made in here, but it's not working.... tempfile.gettempdir()
arcpy.env.scratchWorkspacea = tempfile.mkdtemp(prefix='temp_',dir=config.get('paths','temp_dir'))

print "Setting loghistory to false"
arcpy.SetLogHistory(False)

# buffer distance for input processing extent
buff = config.getint('buffers','sa_processing_buffer')

# Define Solar analyst variables
latitude = '' # generate in for loop from feature attribute
sky_size = int(config.get('solar_analyst','sky_size')) # min is 100

# TODO: Change 2014 to current year
print "Setting SA settings"
time_configuration = arcpy.sa.TimeWholeYear(datetime.date.today().year) # arcgis time object set for all of 2014
day_interval = '' # with whole year analysis default is calendar month
hour_interval = '' # default is 0.5
each_interval = '' # default is no interval (i.e. a single band for whole year)
z_factor = '' # meters for both units, defaults to 1
slope_aspect_input_type = 'FROM_DEM' # how slope/aspect are determined
calculation_directions = int(config.get('solar_analyst','calculation_directions')) # number of directions used when calculating viewshed (multiple of 8 only)
zenith_divisions = int(config.get('solar_analyst','zenith_divisions')) # number of divisions to create sky sectors in sky map
azimuth_divisions = int(config.get('solar_analyst','azimuth_divisions')) # number of divisions to create sky sectors in sky map
diffuse_model_type = 'UNIFORM_SKY' # type of diffuse radiation model
diffuse_proportion = float(config.get('solar_analyst','diffuse_proportion')) # proportion of radiation that is diffuse
transmissivity = float(config.get('solar_analyst','transmissivity')) # fraction of radiation passing through atmosphere (0.5 for generally clear sky)
out_direct_radiation_raster = '' # optional output - direct radiation
out_diffuse_radiation_raster = '' # optional output - diffuse radiation
out_direct_duration_raster = '' # optional output - direct duration


# Database queries to manage processing
reserveQuery = """
UPDATE """ + config.get('postgres','schema') + "." + config.get('postgres','sa_fishnet_table') + """ sa
    SET state=1
    WHERE sa.id in (
        SELECT id FROM """ + config.get('postgres','sa_fishnet_table') + """ WHERE state=0
        ORDER BY ST_Distance(the_geom,ST_SetSrid(ST_MakePoint(""" + config.get('processing','starting_x') + """,""" + config.get('processing','starting_y') + """),""" + config.get('projection','srid') + """))
        LIMIT 1
    )
RETURNING
    id,
    ST_XMin(the_geom) as xmin,
    ST_YMin(the_geom) as ymin,
    ST_XMax(the_geom) as xmax,
    ST_YMax(the_geom) as ymax,
    ST_Y(ST_Transform(ST_CENTROID(the_geom),4326)) AS lat
"""

completeQuery = """
    UPDATE """ + config.get('postgres','schema') + "."  + config.get('postgres','sa_fishnet_table') + """ AS sa
    SET 
    state = c.newstate::integer,
    time = c.runtime::float
    FROM (values
    ('UPDATEVALUES')) AS c(updateid,newstate,runtime)
    WHERE
    sa.id=c.updateid::integer
"""

# connect to database using dbconn connection script
print "Reserving first job"
res = dbconn_quick.run_query(reserveQuery)
count = 0
average = 0

while len(res) > 0:
    resultsToSubmit = []
    for row in res:
        count += 1

        sys.stdout.write("Running Area Solar Radiation for row " + str(row['id']) + "    ")
        start_time = time.clock()

        # add buffer/subtract distance to extent boundaries
        x_min = int(row['xmin']) - buff
        y_min = int(row['ymin']) - buff
        x_max = int(row['xmax']) + buff
        y_max = int(row['ymax']) + buff
        latitude = float(row['lat'])

        # set processing environment
        arcpy.env.extent = arcpy.sa.Extent(x_min, y_min, x_max, y_max)

        # run solar analyst
        try:
            solar_raster = arcpy.sa.AreaSolarRadiation(in_surface_raster, latitude, sky_size, time_configuration, day_interval, hour_interval, each_interval, z_factor, slope_aspect_input_type, calculation_directions, zenith_divisions, azimuth_divisions, diffuse_model_type, diffuse_proportion, transmissivity, out_direct_radiation_raster, out_diffuse_radiation_raster, out_direct_duration_raster)
            # clip to feature extent and saves output
            envelope = "{0} {1} {2} {3}".format(int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax']))
            clipped_solar_raster = out_path + os.sep + 'SRR_' + str(row['id']) + '.img' # what raster format do we want???

            # Delete our output file if it already exists, effectively overwriting it
            if os.path.isfile(clipped_solar_raster):
                os.unlink(clipped_solar_raster)

            if not os.path.isfile(clipped_solar_raster):
                clipped = arcpy.Clip_management(solar_raster, envelope, clipped_solar_raster) #, '', '-3.402823e+038', '', True)

            if os.path.isfile(clipped_solar_raster):
                solarWorked = True

        except 'arcgisscripting.ExecuteError':
            print "\t\t\t" + arcpy.GetMessages(3)
            print sys.exc_info()
            solarWorked = False
        except:   
            print sys.exc_info()
            e = sys.exc_info()[0]
            print "\t\t\t" + str(e)
            solarWorked = False

        # calculate average tile calculation time
        end_time = time.clock()
        time_run = end_time - start_time
        average = (average * (count - 1) + time_run) / count

        if solarWorked:
            print "DONE! (" + str((time_run)) + " seconds, running avg:" + str(average) + ")"
            resultsToSubmit.append([str(row['id']),'2',str(time_run)])
        else:
            print "Error! (" + str((time_run)) + " seconds, running avg:" + str(average) + ")"
            resultsToSubmit.append([str(row['id']),'-3','-1'])

    cq = completeQuery.replace('UPDATEVALUES',"'),('".join(["','".join(x) for x in resultsToSubmit]))
    res = dbconn_quick.send_query(cq)
    res = dbconn_quick.run_query(reserveQuery)

# We have to manually unlink temp dirs created by mkdtemp
shutil.rmtree(arcpy.env.scratchWorkspacea)
shutil.rmtree(arcpy.env.workspace)
