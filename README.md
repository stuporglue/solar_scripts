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
 
1. lasIndex.py -- Create las index files (.lax) for all the laz files.

    python.exe .\steps_sql\lasIndex.py D:\SolarResourceData\MinnesotaLiDAR_LAZ

2. lasbbox2sql.py -- Create an .sql file to insert into PostGIS with buffered bounding boxes for all las. This script uses the laz header info and doesn't calculate the actual exact extent (hence the buffer)

    python.exe .\steps_sql\lasbbox2sql.py D:\SolarResourceData\MinnesotaLiDAR_LAZ data\insert_lidar_bboxes.sql

Insert the resulting sql file into a PostGIS table with the following definition:

    CREATE TABLE lidar_bbox
    (
      id serial NOT NULL,
      lasfile character varying,
      the_geom geometry(Polygon,26915),
      CONSTRAINT lidar_bbox_pkey PRIMARY KEY (id),
      CONSTRAINT lidar_bbox_unique_file UNIQUE (lasfile)
    ) WITH ( OIDS=FALSE);
    CREATE INDEX bbox_gist ON lidar_bbox USING gist (the_geom);

3. las2fishnetSql.py -- Create a fishnet across coordinates which will work with blast2dem, ideally with nice round numbers.

    python.exe .\steps_sql\las2fishnetSql.py D:\SolarResourceData\MinnesotaLiDAR_LAZ 3 10000 data\dem_fishnet.sql

Insert the resulting sql file into a PostGIS table with the following definition:

    CREATE TABLE dem_fishnets
    (
      id serial NOT NULL,
      the_geom geometry(Polygon,26915),
      state integer DEFAULT 0,
      CONSTRAINT dem_fishnets_pkey PRIMARY KEY (id)
    ) WITH ( OIDS=FALSE);
    CREATE INDEX dem_gist ON dem_fishnets USING gist (the_geom);
    CREATE INDEX dem_state_index ON dem_fishnets USING btree (state);

4. Let PostGIS figure rule out any fishnet tiles which don't cover any lidar bounding boxes. Run: 

    UPDATE dem_fishnets 
    SET state=-1 
    WHERE id in (
        SELECT dem.id FROM 
        dem_fishnets dem, 
        lidar_bbox bbox
        WHERE NOT
        ST_Intersects(ST_Buffer(dem.the_geom,100),bbox.the_geom)
    )

5. makeDems.py -- Run as many instances of makeDems.py as you can to create DEM files. blast2dem only uses one cores. As a rule of thumb, run n+1 processes where n is the number of cores you have. 

    python.exe .\steps_sql\makeDems.py D:\SolarResourceData\MinnesotaLiDAR_LAZ D:\SolarResourceData\MinnesotaLiDAR_DSM\fishnet_tiles 

5. dem2mosaic.py -- Convert DSMs to raster mosaic

    Create directory D:\SolarResourceData\MinnesotaLiDAR_DSM\fishnet_mosaic
    python.exe .\steps_sql\dems2mosaic.py D:\SolarResourceData\MinnesotaLiDAR_DSM\fishnet_tiles D:\SolarResourceData\MinnesotaLiDAR_DSM\fishnet_tiles D:\SolarResourceData\MinnesotaLiDAR_DSM\fishnet_mosaic data\MN_Fishnet\MN_Fishnet.prj

6. Create a fishnet across coordinates which will work with Solar Analyist, ideally with nice round numbers. Input the fishnet into PostGIS in a table like this:
    
    CREATE TABLE sa_fishnets
    (
      id serial NOT NULL,
      the_geom geometry(Polygon,26915),
      state integer DEFAULT 0,
      CONSTRAINT sa_fishnets_pkey PRIMARY KEY (id)
    ) WITH ( OIDS=FALSE);
    ALTER TABLE sa_fishnets OWNER TO solar;
    
    CREATE INDEX sa_fishnets_geom_gist ON sa_fishnets USING gist (the_geom);
    CREATE INDEX sa_fishnets_state ON sa_fishnets USING btree (state);


7. batchSolarAnalyst.py -- Runs solar analyst on each sa_fishnet

    tbd

8. Mosaic solar raster tiles to single image?

    tbd
