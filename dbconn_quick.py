#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Version of dbconn that only quickly connects to run a query then disconnects

# Psycopg2 Windows Binaries: http://www.stickpeople.com/projects/python/win-psycopg/
# You probably want the version for Python 2.7 32 bit which is what's distributed with Arc 10.2

from config import *
import psycopg2,psycopg2.extras,os,time,random

host = config.get('postgres','host'), 
port = config.get('postgres','port'), 
database = config.get('postgres','dbname'), 
user = config.get('postgres','user'), 
password = config.get('postgres','pass')

# Run the query and return the results
def run_query(q):
    cur = False
    dbsleeper = 0.3 # start by sleeping for .3 seconds. Sleep at most 5 seconds
    while not cur:
        try:
            conn=psycopg2.connect(host=host,port=port,database=database,user=user,password=password)
            conn.autocommit=True
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        except:
            cur = False
            time.sleep(dbsleeper + random.random())
            if dbsleeper < 5:
                dbsleeper *= 2

    # Now that we have a connection, run the query and return the rows
    try:
        cur.execute(q)
    except Exception as exp:
        print "Exception"
        print exp
        cur.close()
        return []

    rows = cur.fetchall();
    cur.close()
    return rows
