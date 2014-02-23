#!/usr/bin/env python

# GDAL Solar Analyst
#
# Use GDAL to generate a solar radiation map

# Copyright 2014 Michael Moore <stuporglue@gmail.com>

# I got some help from here: http://www.gis.usu.edu/~chrisg/python/2008/os5_slides.pdf

import gdal
from gdalconst import *
import sys
import solar

# Check usage
if len(sys.argv) < 3:
    # List of codes here: http://www.gdal.org/formats_list.html
    sys.exit("USAGE: dsm_solar_analyst.py input.img output.img [GDAL Code for output format]")

inputfile=sys.argv[1] 
outputfile=sys.argv[2]

if len(sys.argv) >= 4:
    output_driver = sys.argv[3]
else:
    # The sample files I have are HFA, so that's what we're going to write by default
    output_driver = 'HFA'

# This should let us read any format
gdal.AllRegister();

# And this will let us write our selected output format
write_driver = gdal.GetDriverByName(output_driver)
write_driver.Register()

# Open the file
dsm = gdal.Open(inputfile,GA_ReadOnly)

# Verify that file is opened
if dsm is None:
    sys.exit("Could not open file " + inputfile)

cols = dsm.RasterXSize
rows = dsm.RasterYSize
bands = dsm.RasterCount

# Friendly warning
if bands > 1:
    sys.stderr.write("WARNING: " + inputfile + " has more than a single band. The first band will be used")

# Assume that we want the first band
band = dsm.GetRasterBand(1)

# Assume that we can hold the whole DSM in memory
# Data is a numpy.ndarray
data = band.ReadAsArray(0,0,cols,rows)

solar = solar(data)
outdata = solar.globalTotalRadiation()

# Output untested. This all came from here
# http://stackoverflow.com/questions/6710368/gdal-raster-output
outhandle = write_driver.Create(outfile,cols,rows,1,GDT_Int32)
if outhandle is None:
    sys.exit("Could not open file " + outfile)

outBand = outhandle.GetRasterBand(1)
outBand.WriteArray(outdata)
outBand.FlushCache()
outBand.SetNoDataValue(-99)
outBand.setGeoTransform(dsm.GetGeoTransform())
outBand.setProjection(dsm.GetProjection()) # In our case I think our projections are labeled incorrectly
