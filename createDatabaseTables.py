# TODO: Create statements for database

import os,dbconn
from config import *

schema = config.get('postgres','schema')

sqls = []
sqls.append("""
CREATE TABLE """ + schema + "." + config.get('postgres','dem_fishnet_table') + """
(
  id serial,
  the_geom geometry(Polygon,""" + config.get('projection','srid') + """),
  state integer DEFAULT 0,
  CONSTRAINT dem_fishnets_pkey PRIMARY KEY (id)
) WITH (OIDS=FALSE)
""")

sqls.append("CREATE INDEX dem_gist ON " + schema + "." + config.get('postgres','dem_fishnet_table') + " USING gist (the_geom)")
sqls.append("CREATE INDEX dem_state_index ON " + schema + "." + config.get('postgres','dem_fishnet_table') + " USING btree (state)")

sqls.append("""
CREATE TABLE """ + schema + "." + config.get('postgres','lidar_bbox_table') + """
(
  id serial,
  lasfile character varying,
  the_geom geometry(Polygon,""" + config.get('projection','srid') + """),
  CONSTRAINT lidar_bbox_pkey PRIMARY KEY (id),
  CONSTRAINT lidar_bbox_unique_file UNIQUE (lasfile)
) WITH (OIDS=FALSE)
""")

sqls.append("CREATE INDEX bbox_gist ON " + schema + "." + config.get('postgres','lidar_bbox_table') + " USING gist (the_geom)")

sqls.append("""
CREATE TABLE """ + schema + "." + config.get('postgres','sa_fishnet_table') + """ 
(
  id serial,
  the_geom geometry(Polygon,""" + config.get('projection','srid') + """),
  state integer DEFAULT 0,
  "time" double precision,
  CONSTRAINT sa_fish2_pkey PRIMARY KEY (id)
) WITH (OIDS=FALSE)
""")

sqls.append("CREATE INDEX sa_fish2_geom_gist ON " + schema +  "." + config.get('postgres','sa_fishnet_table') + " USING gist (the_geom)")
sqls.append("CREATE INDEX sa_fishnet_state ON " + schema + "." + config.get('postgres','sa_fishnet_table') + " USING btree (state)")

for sql in sqls:
    print sql
    print ""
    if not dbconn.run_query(sql):
        print "ERROR!"
        exit()

print "Done!"
