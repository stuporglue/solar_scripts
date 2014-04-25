# Create a Mosaic Dataset in the workspace and add all 
# *.img rasters from the input directory
#
# python dems2mosaic.py "C:\workspace\dems" "C:\workspace" "26915.prj"

import arcpy,sys,os
from config import *
from distutils.spawn import *
from arcpy import *

################ Usage check and argument assigning
if len(sys.argv) != 4:
    print "Usage: build_mosaic.py <input directory> <workspace/output dir> <.prj file>"
    print "The input directory should have the img rasters in it"
    print "Contents in the output directory will be overwritten"
    exit(-1)
else:
    inpath = config.get('paths','dem_output_dir')
    workspacedir = config.get('arcgis','workspace')
    prjfile = config.get('projection','prj_file')

arcpy.env.workspace = workspacedir
gdbname = config.get('arcgis','dem_mosaic_name')

# Create a File GeoDatabase to house the Mosaic dataset
arcpy.CreateFileGDB_management(workspacedir, gdbname)

# Create Mosaic Dataset
# http://resources.arcgis.com/en/help/main/10.2/index.html#//00170000008n000000

mdname = "DEM_MOSAIC"
noband = "1"
pixtype = "32_BIT_FLOAT"
pdef = "NONE"
wavelength = ""

arcpy.CreateMosaicDataset_management(gdbname, mdname, prjfile, noband, pixtype, pdef, wavelength)


# Add rasters to Mosaic Dataset
# http://resources.arcgis.com/en/help/main/10.2/index.html#//001700000085000000

mdname = gdbname + "/" + mdname
rastype = "ERDAS IMAGINE"  # http://resources.arcgis.com/en/help/main/10.2/index.html#//009t0000000v000000

updatecs = "NO_CELL_SIZES"
updatebnd = "NO_BOUNDARY"
updateovr = "UPDATE_OVERVIEWS"
maxlevel = "0"  # pyramid level
maxcs = ""
maxdim = ""
spatialref = ""
inputdatafilter = "*.img"
subfolder = "NO_SUBFOLDERS"
duplicate = "EXCLUDE_DUPLICATES"
buildpy = "NO_PYRAMIDS"
calcstats = "NO_STATISTICS"  # CALCULATE_STATISTICS
buildthumb = "NO_THUMBNAILS"
comments = "Add Raster Datasets"
forcesr = "NO_FORCE_SPATIAL_REFERENCE"

arcpy.AddRastersToMosaicDataset_management(
     mdname,  rastype, inpath, updatecs, updatebnd, updateovr,
     maxlevel, maxcs, maxdim, spatialref, inputdatafilter,
     subfolder, duplicate, buildpy, calcstats, 
     buildthumb, comments, forcesr)
