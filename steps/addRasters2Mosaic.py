import arcpy, time

ws = 'F:\\SolarResourceData\\MinnesotaLiDAR_DSM\\fishnet_tiles'
arcpy.env.workspace = ws

# inList = arcpy.ListRasters('*.img')

mdname = 'F:\\SolarResourceData\\MinnesotaLiDAR_DSM\mosaic_dem\\MN_DEM.gdb\\MN_DSM'
rastype = "Raster Dataset" # http://resources.arcgis.com/en/help/main/10.2/index.html#//009t0000000v000000

updatecs = "UPDATE_CELL_SIZES"
updatebnd = "UPDATE_BOUNDARY"
updateovr = "UPDATE_OVERVIEWS"
maxlevel = "0" # pyramid level
maxcs = ""
maxdim = ""
spatialref = ""
inputdatafilter = "*.img"
subfolder = "NO_SUBFOLDERS"
duplicate = "EXCLUDE_DUPLICATES"
buildpy = "BUILD_PYRAMIDS"
calcstats = "CALCULATE_STATISTICS" # CALCULATE_STATISTICS
buildthumb = "No_THUMBNAILS"
comments = "Add Raster Datasets"
forcesr = "NO_FORCE_SPATIAL_REFERENCE"

# for ras in inList:
time1 = time.time()
arcpy.AddRastersToMosaicDataset_management(
 mdname, rastype, ws, updatecs, updatebnd, updateovr,
 maxlevel, maxcs, maxdim, spatialref, inputdatafilter,
 subfolder, duplicate, buildpy, calcstats,
 buildthumb, comments, forcesr)
timeDif = time.time() - time1
print "Done with raster {0} in {1} seconds".format(str('Folder'), round(timeDif, 2))
