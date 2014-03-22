# Create a Mosaic Dataset in the workspace and add all 
# *.img rasters from the input directory
#
# python dems2mosaic.py "C:\workspace\dems" "C:\workspace" "26915.prj"

import arcpy, sys, os
from distutils.spawn import *
from arcpy import *


################ Usage check and argument assigning
if len(sys.argv) != 4:
    print "Usage: build_mosaic.py <input directory> <workspace/output dir> <.prj file>"
    print "The input directory should have the img rasters in it"
    print "Contents in the output directory will be overwritten"
    exit(-1)
else:
    inpath = sys.argv[1]
    workspacedir = sys.argv[2]
    prjfile = sys.argv[3]

if not os.path.isdir(inpath):
    print "Input directory must be a directory and exist"
    exit(-1)

if not os.path.isdir(workspacedir):
    print "Workspace directory must be a directory and exist"
    exit(-1)

if not os.path.isfile(prjfile):
    print "You must provide a valid prj file"
    exit(-1)
    
arcpy.env.workspace = workspacedir
gdbname = "MN_DEM.gdb"


# Create a File GeoDatabase to house the Mosaic dataset
arcpy.CreateFileGDB_management(workspacedir, gdbname)

# Create Mosaic Dataset
# http://resources.arcgis.com/en/help/main/10.2/index.html#//00170000008n000000

mdname = "MN_MD"
noband = "1"
pixtype = "32_BIT_FLOAT"
pdef = "NONE"
wavelength = ""

arcpy.CreateMosaicDataset_management(gdbname, mdname, prjfile, noband, 
                                     pixtype, pdef, wavelength)


# Add rasters to Mosaic Dataset
# http://resources.arcgis.com/en/help/main/10.2/index.html#//001700000085000000

mdname = gdbname + "/" + mdname
rastype = "Raster Dataset"  # http://resources.arcgis.com/en/help/main/10.2/index.html#//009t0000000v000000

updatecs = "NO_CELL_SIZES"
updatebnd = "NO_BOUNDARY"
updateovr = "NO_OVERVIEWS"
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
