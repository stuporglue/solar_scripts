#!/bin/bash

export PATH=/home/lenkne/shared/arc/server/arcgis/server/tools/:$PATH
export LD_LIBRARY_PATH=/home/lenkne/shared/arc/libs:$LD_LIBRARY_PATH
export LOGNAME=moor1090

while true; do 
    /home/lenkne/shared/arc/server/arcgis/server/tools/python /home/lenkne/shared/solar_scripts/batchSolarAnalyst.py
    echo "----------------------   Python or Wine probably crashed. Sleeping for a bit then trying again -----------------------"
    sleep $(( ( RANDOM % 10 )  + 10 ))
done
