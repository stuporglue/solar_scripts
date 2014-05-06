#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Psycopg2 Windows Binaries: http://www.stickpeople.com/projects/python/win-psycopg/
# You probably want the version for Python 2.7 32 bit which is what's distributed with Arc 10.2

from config import *
import psycopg2,psycopg2.extras,os,simplejson as json
from psycopg2.extensions import adapt

try:
    conn = psycopg2.connect(
            host = config.get('postgres','host'), 
            port = config.get('postgres','port'), 
            database = config.get('postgres','dbname'), 
            user = config.get('postgres','user'), 
            password = config.get('postgres','pass')
            )
    conn.autocommit=True

    # Create a server-side cursor so we don't end up with all records in memory at once
    # http://wiki.postgresql.org/wiki/Using_psycopg2_with_PostgreSQL 
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
except Exception as e:
    print "Unable to connect to the database"
    print e
    exit()

def rewind():
    return cur.scroll(0,mode='absolute')

# Run the query and return the results
def run_query(q):
    try:
        cur.execute(q)
    except Exception as exp:
        print "Exception"
        print exp
        
    return cur

# Run the query and print the results as GeoJSON
def send_query(q):
    cur = run_query(q)
    geojson = array_to_geojson(cur)
    return send_array_as_json(geojson)

# Turn a cursor into an object.
def cursor_to_object(rows,idfield):
    ret = {}
    for row in rows:
        tmpobj = {}
        for k in row.keys():
            tmpobj[k] = row[k]
        ret[row[idfield]] = tmpobj

    return ret

# Turn an array into GeoJSON. Assumes that the geometry field was requested as ST_AsGeoJson(the_geom) AS the_geom
def array_to_geojson(rows):
    # Build an empty GeoJSON FeatureCollection object, then fill it from the database results
    output = {
            'type' : 'FeatureCollection',
            'features' : []
    }

    for row in rows:
        # Make a single feature
        one = {
                'type' : 'Feature',
                'geometry' : json.loads(row['the_geom']),
                'properties' : {}
        }

        # Apply its properties
        for k in row.keys():
            if k != 'the_geom':
                one['properties'][k] = row[k]

        # Stick it in our collection
        output['features'].append(one)
    return output

# Print n array as GeoJSON 
def send_array_as_json(arr):
    # First we have to print some headers
    # Followed by two blank lines. That's how the browser knows the headers are all done
    print "Content-Type: application/json; charset=utf-8"
    print

    # Encode resulting object as json
    js = json.dumps(arr,separators=(',',':'))
    print js
    return js
