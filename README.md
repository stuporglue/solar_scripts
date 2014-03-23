Solar Scripts 
=============

Warning: Probably none of this works right now
These are scripts developed for GIS 8890, a directed studies course in the MGIS program at the University of Minnesota

The goal of our project is to create a state-wide solar suitability map from lidar data.

We settled on using lastools and ArcGIS (via ArcPy) for this project. 

We started with roughly 1Tb of .laz files, available from the state of [Minnesota's FTP site](http://www.mngeo.state.mn.us/chouse/elevation/lidar.html).

Below is the current pseudo code

How We're Doing It
----------------------

These aren't instructions so much as what we're doing. Your data will probably break in different ways than ours. This code is unsupported, so here's what worked for us, hopefully it'll put you on the right path. 

1. Configure the database connection file. 
   
   Copy dbconn.cfg.example to dbconn.cfg and replace the existing values with the values for your PostGIS database connection.

 
2. lasIndex.py -- Create las index files (.lax) for all the laz files.

        python.exe .\steps_sql\lasIndex.py D:\SolarResourceData\MinnesotaLiDAR_LAZ

3. lasbbox2sql.py -- Create an .sql file to insert into PostGIS with buffered bounding boxes for all las. This script uses the laz header info and doesn't calculate the actual exact extent (hence the buffer)

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

4. las2fishnetSql.py -- Create a fishnet across coordinates which will work with blast2dem, ideally with nice round numbers.

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

5. Let PostGIS figure rule out any fishnet tiles which don't cover any lidar bounding boxes. Run: 

        UPDATE dem_fishnets 
        SET state=-1 
        WHERE id in (
            SELECT dem.id FROM 
            dem_fishnets dem, 
            lidar_bbox bbox
            WHERE NOT
            ST_Intersects(ST_Buffer(dem.the_geom,100),bbox.the_geom)
        )


6. makeDems.py -- Run as many instances of makeDems.py as you can to create DEM files. blast2dem only uses one cores. Balance disk IO, memory and CPU usage to get the best average times you can.

        python.exe .\steps_sql\makeDems.py D:\SolarResourceData\MinnesotaLiDAR_LAZ D:\SolarResourceData\MinnesotaLiDAR_DSM\fishnet_tiles 
        
    !["Running 8 instances and getting nearly 100% CPU usage"](https://raw.githubusercontent.com/stuporglue/solar_scripts/master/web/dev/img/Parallell_DSM_Creation.png "Running 8 instances and getting nearly 100% CPU usage")

7. dem2mosaic.py -- Convert DSMs to raster mosaic

    Create directory D:\SolarResourceData\MinnesotaLiDAR_DSM\fishnet_mosaic

        python.exe .\steps_sql\dems2mosaic.py D:\SolarResourceData\MinnesotaLiDAR_DSM\fishnet_tiles D:\SolarResourceData\MinnesotaLiDAR_DSM\fishnet_tiles D:\SolarResourceData\MinnesotaLiDAR_DSM\fishnet_mosaic data\MN_Fishnet\MN_Fishnet.prj

8. Create a fishnet across coordinates which will work with Solar Analyist, ideally with nice round numbers. Input the fishnet into PostGIS in a table like this:

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

9. batchSolarAnalyst.py -- Runs solar analyst on each sa_fishnet

        tbd

10. Mosaic solar raster tiles to single image?

        tbd


Web Progress Viewer
------------------

A progress viewer website is available in this repository. You will need to configure your server to treat .py files as CGI executables. It uses Leaflet.js to display the progress.
 
!["Fishnets being processed outwards from Blegen Hall"](https://raw.githubusercontent.com/stuporglue/solar_scripts/master/web/dev/img/DSM_Progress_clipped.png "Fishnets being processed outwards from Blegen Hall")
