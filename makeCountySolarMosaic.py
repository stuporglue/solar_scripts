# Python script to make a raster mosaic for a single county


import arcpy, sys, os, glob, time
from distutils.spawn import *

basedir = "\\\\files.umn.edu\\US-MGIS-Lidar\\SA_Tiles_By_County\\"

for countyname_with_spaces in glob.glob(basedir + '*'):
    countyname_with_spaces = os.path.basename(countyname_with_spaces)
    countyname = countyname_with_spaces.replace(' ','_')

    if countyname_with_spaces.find('.') != -1:
        print countyname_with_spaces + " has dots in the name, it's probably a gdb or something"
        continue

    if os.path.isdir(basedir + countyname_with_spaces + "\\" + countyname+".gdb"):
        print countyname_with_spaces + " already has a gdb. Not processing."
        continue

    os.path.getmtime(basedir + countyname_with_spaces)

    if((time.time() - os.path.getmtime(basedir + countyname_with_spaces))  < 600):
        print countyname_with_spaces + " was modified in the last 10 minutes. Skipping for now."
        continue

    print "Processing " + countyname

    workspacedir = basedir + countyname_with_spaces + "\\"
    arcpy.env.workspace = workspacedir

    # Create a File GeoDatabase to house the Mosaic dataset
    print "Creating GDB File"
    arcpy.CreateFileGDB_management(workspacedir, countyname + '.gdb')

    # Create Mosaic Dataset
    # http://resources.arcgis.com/en/help/main/10.2/index.html#//00170000008n000000
    print "Creating mosaic dataset"
    arcpy.CreateMosaicDataset_management(basedir + countyname_with_spaces + "\\" + countyname + ".gdb",countyname,"PROJCS['NAD_1983_UTM_Zone_15N',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-93.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]];-5120900 -9998100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision","#","#","NONE","#")
    
    print "Adding rasters"
    arcpy.AddRastersToMosaicDataset_management(basedir + countyname_with_spaces + "\\" + countyname + ".gdb\\" + countyname,"Raster Dataset",basedir + countyname_with_spaces,"UPDATE_CELL_SIZES","UPDATE_BOUNDARY","NO_OVERVIEWS","#","0","1500","#","#","SUBFOLDERS","ALLOW_DUPLICATES","NO_PYRAMIDS","NO_STATISTICS","NO_THUMBNAILS","#","NO_FORCE_SPATIAL_REFERENCE")
    
    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
    # The following inputs are layers or table views: countyname
    # I don't think we need to analyze since we know what should need to be run
    # arcpy.AnalyzeMosaicDataset_management(countyname,"#","FOOTPRINT;FUNCTION;RASTER;PATHS;SOURCE_VALIDITY;STALE;PYRAMIDS;STATISTICS;PERFORMANCE;INFORMATION")

    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
    # The following inputs are layers or table views: countyname
    print "Build overviews"
    arcpy.BuildOverviews_management(basedir + countyname_with_spaces + "\\" + countyname + ".gdb\\" + countyname,"#","DEFINE_MISSING_TILES","GENERATE_OVERVIEWS","GENERATE_MISSING_IMAGES","REGENERATE_STALE_IMAGES")

    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
    # The following inputs are layers or table views: countyname
    print "Calculating statistics"
    arcpy.CalculateStatistics_management(basedir + countyname_with_spaces + "\\" + countyname + ".gdb\\" + countyname,"1","1","#","OVERWRITE","Feature Set")

    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
    # The following inputs are layers or table views: countyname
    print "Calc stats 1"
    arcpy.BuildPyramidsandStatistics_management(basedir + countyname_with_spaces + "\\" + countyname + ".gdb\\" + countyname,"INCLUDE_SUBDIRECTORIES","NONE","CALCULATE_STATISTICS","NONE","#","NONE","1","1","#","-1","NONE","NEAREST","DEFAULT","75","SKIP_EXISTING")


    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
    # The following inputs are layers or table views: countyname
    print "Building pyramids"
    arcpy.BuildPyramidsandStatistics_management(basedir + countyname_with_spaces + "\\" + countyname + ".gdb\\" + countyname,"INCLUDE_SUBDIRECTORIES","BUILD_PYRAMIDS","NONE","BUILD_ON_SOURCE","#","NONE","1","1","#","-1","NONE","NEAREST","DEFAULT","75","SKIP_EXISTING")

    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
    # The following inputs are layers or table views: countyname
    print "Calc stats 2"
    arcpy.BuildPyramidsandStatistics_management(basedir + countyname_with_spaces + "\\" + countyname + ".gdb\\" + countyname,"INCLUDE_SUBDIRECTORIES","NONE","CALCULATE_STATISTICS","BUILD_ON_SOURCE","#","NONE","1","1","#","-1","NONE","NEAREST","DEFAULT","75","SKIP_EXISTING")
