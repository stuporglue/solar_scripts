#!/usr/bin/env python

# Psycopg2 Windows Binaries: http://www.stickpeople.com/projects/python/win-psycopg/
# You probably want the version for Python 2.7 32 bit which is what's distributed with Arc 10.2

import psycopg2
import psycopg2.extras
from psycopg2.extensions import adapt
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open('dbconn.cfg'))

try:
    conn = psycopg2.connect(host = config.get('auth','host'), port = config.get('auth','port'), database = config.get('auth','dbname'), user = config.get('auth','user'), password = config.get('auth','pass'))

    # Create a server-side cursor so we don't end up with all records in memory at once
    # http://wiki.postgresql.org/wiki/Using_psycopg2_with_PostgreSQL 
    cur = conn.cursor('dbconn', cursor_factory=psycopg2.extras.RealDictCursor,scrollable=True)
except Exception as e:
    print "Unable to connect to the database"
    print e
    exit()

def rewind():
    return cur.scroll(0,mode='absolute')

def run_query(q):
    cur.execute(q)
    return cur
