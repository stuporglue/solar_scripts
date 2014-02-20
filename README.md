Solar Scripts
=============

Probably none of this works right now. 

These are some scripts for a solar project at school.

 * las_to_dsm_batch.py -- Take a list of files and processe them with child processes. You can define the script to be run and the max number of children. Configured to run las2dem on my personal machine. 
 * gdal_solar_analyst.py -- Input a raster readable by gdal and run solar.py's globalTotalRadiation function on it to produce a new output raster
 * las2dsm.py -- Convert las/laz to dsm files using grass's v.in.lidar
 * solar.py -- Python implementation of the solar radiation calculations [used by Esri's Solar Analyst](http://resources.arcgis.com/en/help/main/10.1/index.html#//009z000000tm000000)

