#!/bin/bash

export PATH=/home/lenkne/shared/arc/server/arcgis/server/tools/:$PATH
export LD_LIBRARY_PATH=/home/lenkne/shared/arc/libs:$LD_LIBRARY_PATH
export LOGNAME=moor1090

MAXTRIES=100

export DOTWINE="/lustre/moor1090/$(hostname)$RANDOM$$"
cp -r /lenkne/shared/arc/server/arcgis/server/framework/runtime/.wine $DOTWINE

while [[ $MAXTRIES -gt 0 ]]; do 
    /home/lenkne/shared/arc/server/arcgis/server/tools/python /home/lenkne/shared/solar_scripts/batchSolarAnalyst.py
    echo "$(hostname) - wine down again ($MAXTRIES tries left) -"
    sleep $(( ( RANDOM % 10 )  + 10 ))
    ((MAXTRIES--))
done

echo "$(hostname) I tried to start python/wine 100 times. I'm giving up and going home."
