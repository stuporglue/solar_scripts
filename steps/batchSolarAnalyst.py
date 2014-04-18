# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# batchSolarAnalyst.py
# Created on: 2014-16-08 
# Description: Generate solar radiation tiles for all areas in a shapefile
# ---------------------------------------------------------------------------

# "Calculate solar radiation over a very large area by using a Raster Dataset and using a shapefile of polygons to choose which areas
# to use as extents when calculating areas for.
# Also accepts a buffer size which will be applied to each polygon for use in the extent.
# The final image output will be clipped back to the size of the input polygon
# print "USAGE batchSolarAnalyst.py <Workspace path> <Mosaic Raster Dataset> <Output path>"


# Pseudo Code!
# For eachPolygon in Shapefile:
# bufferedPollygon = buffer polygon by bufferAmount
# set extent env to bufferedPolygon
# outputRaster = AreaSolarRadiation(rasterDataset)
# clippedOutput = clip outputRaster back to polygon size
# write clippedOutput file to designated directory?

import sys, os, arcpy, time, dbconn

##if len(sys.argv) != 4:
##    print "Usage batchSolarAnalyst.py <basedir> <mosaicdem> <outputdir>\
##\n\t<basedir> - file path to the base directory, for arcpy workspace environment\
##\n\t<mosaicdem> - file name for mosaic raster – if not in the <basedir> include path\
##\n\t<outputdir> - folder location to save output files to"
##    exit(-1)


# Define workspace and input datasets
ws = sys.argv[1]
inMosaicDEM = sys.argv[2]
out_path = sys.argv[3]


# Check out spatial analyst and set ArcGIS environment settings
arcpy.CheckOutExtension("spatial")
arcpy.env.workspace = ws
arcpy.SetLogHistory(True)


# buffer distance for input processing extent
buff = 50


# Define Solar analyst variables
in_surface_raster = inMosaicDEM
latitude = '' # generate in for loop from feature attribute
sky_size = 100 # min is 100
time_configuration = arcpy.sa.TimeWholeYear(2014) # arcgis time object set for all of 2014
day_interval = '' # with whole year analysis default is calendar month
hour_interval = '' # default is 0.5
each_interval = '' # default is no interval (i.e. a single band for whole year)
z_factor = '' # meters for both units, defaults to 1
slope_aspect_input_type = 'FROM_DEM' # how slope/aspect are determined
calculation_directions = 32 # number of directions used when calculating viewshed (multiple of 8 only)
zenith_divisions = 8 # number of divisions to create sky sectors in sky map
azimuth_divisions = 8 # number of divisions to create sky sectors in sky map
diffuse_model_type = 'UNIFORM_SKY' # type of diffuse radiation model
diffuse_proportion = 0.3 # proportion of radiation that is diffuse
transmissivity = 0.5 # fraction of radiation passing through atmosphere (0.5 for generally clear sky)
out_direct_radiation_raster = '' # optional output - direct radiation
out_diffuse_radiation_raster = '' # optional output - diffuse radiation
out_direct_duration_raster = '' # optional output - direct duration


# Database queries to manage processing
reserveQuery = """
UPDATE sa_fishnets sa
SET state=1
WHERE sa.id in (
SELECT id FROM sa_fishnets WHERE state=0
ORDER BY ST_Distance(the_geom,ST_SetSrid(ST_MakePoint(480815.0,4979852.6),26915))
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
    UPDATE 
    sa_fishnets sa
    SET state=NEWSTATE,
    time = x
    WHERE
    sa.id=DEMID
"""

# connect to database using dbconn connection script
res = dbconn.run_query(reserveQuery).fetchall()
count = 0
average = 0

while len(res) > 0:
    for row in res:
        count += 1
        
        sys.stdout.write("Running Area Solar Radiation for row " + str(row['id']))
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
            clipped_solar_raster = out_path + 'SRR_' + str(row['id']) + '.img' # what raster format do we want???

            # print "Saving unclipped version to: " + out_path + 'SRR_' + str(row['id']) + "_unclipped.img"            
            # solar_raster.save(out_path + 'SRR_' + str(row['id']) + "_unclipped.img")
            
            print "Saving clipped version to: " + clipped_solar_raster            
            clipped = arcpy.Clip_management(solar_raster, envelope, clipped_solar_raster) #, '', '-3.402823e+038', '', True)
            solarWorked = True

        except:   
            e = sys.exc_info()[0]
            print "\t\t\t" + str(e)
            solarWorked = False
            
        # calculate average tile calculation time
        end_time = time.clock()
        time_run = end_time - start_time
        average = (average * (count - 1) + time_run) / count
        
        if solarWorked:
            print "DONE! (" + str((time_run)) + " seconds, running avg:" + str(average) + ")"
            dbconn.run_query(completeQuery.replace("DEMID",str(row['id'])).replace('NEWSTATE','2').replace('x', str(time_run)))
        else:
            print "Error! (" + str((stoptime - starttime)) + " seconds, running avg:" + str(average) + ")"
            dbconn.run_query(completeQuery.replace("DEMID",str(row['id'])).replace('NEWSTATE','-3'))


        print "Clipped returned: " + str(clipped)

        # save raster object
        #clipped_solar_raster.save(out_path + 'SRR_' + featureID + '.img')
        

        
        # print summary information to command prompt
        result = "Processed fishnet section {0} in {1} seconds, with an overall average time of {2}".format(str(row['id']), round(time_run, 2), round(average, 2))
        print result
        
    res = dbconn.run_query(reserveQuery).fetchall()

del res
