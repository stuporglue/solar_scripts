Solar Scripts 
=============

Warning: Probably none of this works right now
These are scripts developed for GIS 8890, a directed studies course in the MGIS program at the University of Minnesota

The goal of our project is to create a state-wide solar suitability map from lidar data.

We settled on using lastools and ArcGIS (via ArcPy) for this project. 

We started with roughly 1Tb of .laz files, available from the state of [Minnesota's FTP site](http://www.mngeo.state.mn.us/chouse/elevation/lidar.html).

Below is the current pseudo code

Pseudo Code 
-----------
 
1. lasIndex.py -- Index all .laz files (lasindex)
2. las2fishnet.py -- Get the coordinates of all laz files toogether (lasinfo)
3. las2fishnet.py -- Create a fishnet across coordinates which will work with blast2dem, ideally with nice round numbers 
4. blast2dem all fishnet buffered output to dsms
5. Convert DSMs to raster mosaic
6. Create a fishnet across coordinates which will work with Solar Analyist, ideally with nice round numbers or matching input 256k grids
7. Solar Analyist all fishnets to solar raster tiles
8. Mosaic solar raster tiles to single image?

Generate The Solar Data
-----------------------
These are actual commands. You might need to modify them for your enviornment

Laz file locations: lidarData\q????\laz\*.laz

1. python.exe .\steps\lasIndex.py .\lidarData
2. python.exe .\steps\las2fishnet.py .\lidarData 3 10000 fishnet.csv
3. python.exe .\steps\fishnet2blast.py .\lidarData .\output .\fishnet.csv

