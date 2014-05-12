#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Version of dbconn that only quickly connects to run a query then disconnects

# Psycopg2 Windows Binaries: http://www.stickpeople.com/projects/python/win-psycopg/
# You probably want the version for Python 2.7 32 bit which is what's distributed with Arc 10.2

from config import *
import psycopg2,os,time
import psycopg2.extras
#psycopg2.extras,os,time

#from psycopg2.extensions import adapt

host = config.get('postgres','host')
port = config.get('postgres','port')
database = config.get('postgres','dbname')
user = config.get('postgres','user')
password = config.get('postgres','pass')

def _getConn():
    cur = False
    print "Trying to connect to the database"
    while not cur:
        try:
            args = {
                    'host':host,
                    'port':port,
                    'database':database,
                    'user':user,
                    'password':password
                    }
            conn=psycopg2.connect(**args)
            print "Successfuly connected to the db"
            conn.autocommit=True
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            #cur = conn.cursor()
            print "Here's a cursor"
            return cur
        except:
            print "Failed as " + str(cur) + ' ' + str(sys.exc_info()[0])
            print "Sleeping for " + str(dbsleeper)
            cur = False
            time.sleep(dbsleeper + time() % 1)
            if dbsleeper < 5:
                dbsleeper *= 2



# Run the query and return the results
def run_query(q):
    cur = False
    dbsleeper = 0.3 # start by sleeping for .3 seconds. Sleep at most 5 seconds
    while not cur:

        cur = _getConn()

        if cur:
            # Now that we have a connection, run the query and return the rows
            try:
                cur.execute(q)
                rows = cur.fetchall();
                cur.close()
                return rows
            except Exception as exp:
                print "Exception"
                print exp
                time.sleep(dbsleeper + time() % 1)


# Run the query and don't return the results
def send_query(q):
    cur = False
    dbsleeper = 0.3 # start by sleeping for .3 seconds. Sleep at most 5 seconds
    while not cur:
        cur = _getConn()

        if cur:
            # Now that we have a connection, run the query and return the rows
            try:
                cur.execute(q)
                cur.close()
                return True 
            except Exception as exp:
                print "Exception"
                print exp
                time.sleep(dbsleeper + time() % 1)
