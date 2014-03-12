https://groups.google.com/forum/#!topic/lastools/RLBoiKd3I6g


blast2dem 
-i *.laz 
-merged 
-keep_classification 2 
-inside 469950 4480000 495000 4520000 
-ll 470000 4480000 -ncols 25000 -nrows 40000 
-o "C:\dtm\DTM1m_east.img"


blast2dem 
-i *.laz 
-merged 
-keep_classification 2 
-inside 450000 4480000 471050 4520000
-ll 450000 4480000 -ncols 30000 -nrows 40000
-odir "C:\dtm\DTM1m_west.img"

Pseudo code: 

1) Index all .laz files (lasindex)
2) Get the coordinates of all laz files toogether (lasinfo)
3) Create a fishnet across coordinates which will work with blast2dem, ideally with nice round numbers 
4) blast2dem all fishnet buffered output to dsms
5) Convert DSMs to raster mosaic
6) Create a fishnet across coordinates which will work with Solar Analyist, ideally with nice round numbers or matching input 256k grids
7) Solar Analyist all fishnets to SA raster tiles


