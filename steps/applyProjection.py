import arcpy

sr = arcpy.SpatialReference("NAD 1983 UTM Zone 15N")
arcpy.env.workspace = 'F:\\SolarResourceData\\MinnesotaLiDAR_DSM\\fishnet_tiles'

inList = arcpy.ListRasters()

for ras in inList:
    arcpy.DefineProjection_management(ras, sr)
    print "projected file {0}".format(str(ras))
print inList
