#!/usr/bin/env python

# Batch convert laz files into DEMs using multiple processes
# "USAGE: las_to_dem.py input.laz [input2.laz,...]"

# If you have enough RAM, you probably want 2 kids per CPU core
# This is because most cores have hyperthreading and act similar to 2 cores
MAXKIDS=8

# Leave this empty to put the DEM next to the original input file or specify a directory
OUTPUTDIR="dems"

# change this command to reflect your desired las2dem arguments
# SRCFILE will be replaced with the full path to the input file 
# FILENAME will be replaced with the base name of the input file (eg /home/michael/lasfiles/tile1.laz would become tile1.laz)
# OUTPUTDIR will be replaced with the value of the variable OUTPUTDIR
LASCOMMAND="wine /opt/lastools/bin/las2dem -i SRCFILE -first_only -step 1.0 -hillshade -o OUTPUTDIR/FILENAME.png"




import sys
import os
from subprocess import call
import signal
import time

# First arg is script name
tiles = sys.argv[1:]

if len(tiles) == 0:
    print "USAGE: las_to_dem.py input.laz [input2.laz,...]"
    exit(0)


keep_looping = True

# These are our child processes
children = []

# final cleanup to run if ctrl-c is pressed
def processKilledCleanup():
    # Stop new children from spawning
    keep_looping = false

    # Send ctrl-c signal to all children
    for child in children:
        os.kill(child,signal.SIGINT)

    # reap children
    for i,child in enumerate(children):
        os.waitpid(child)

    # exit
    sys.exit(0)
    
signal.signal(signal.SIGINT, processKilledCleanup)

# Keep processing while we have more tiles to process
while(len(tiles) > 0 and keep_looping):

    # If we have any child slots left, make a new child
    if len(children) < MAXKIDS:

        # Grab a tile for the child to process
        curtile = tiles.pop()
        
        # Child creation....now
        pid = os.fork()
        if pid:
            # This is the parent process. It just saves the child's 
            # Process ID number, then goes back to the loop
            children.append(pid)
        else:
            # The child calls las2dem
            # this call needs to be updated for the actual machine it will run on
            # The settings below are for my machine
            cmd = LASCOMMAND.replace('OUTPUTDIR',OUTPUTDIR).replace('SRCFILE',curtile).replace('FILENAME',os.path.basename(curtile))
            call(cmd,shell=True);

            # The child exits when it is done
            sys._exit(0)
    else:
        # On every loop iteration we check on our kids
        # If any child has exited, we remove them from 
        # our children list to make room for a new child
        for child in children:
            resp = os.waitpid(child,os.WNOHANG) # If child is done, returns a tuple: [child pid, exit status]
            if resp[0] != 0:
                # Child has exited. 
                children.remove(child)

        # Wait a second so we don't just loop like crazy
        time.sleep(1)

# When all the tiles are done, we need to reap the remaining children
for i,child in enumerate(children):
    os.waitpid(child)
