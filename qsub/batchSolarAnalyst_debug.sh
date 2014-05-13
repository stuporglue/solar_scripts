#!/bin/bash

export PATH=/home/lenkne/shared/arc/server/arcgis/server/tools/:$PATH
export LD_LIBRARY_PATH=/home/lenkne/shared/arc/libs:$LD_LIBRARY_PATH
export LOGNAME=moor1090
export WINEDEBUG="-all"

MAXTRIES=100

FAKEWINETOP="/lustre/moor1090/$(hostname)$RANDOM$$"

echo "Copying .wine directory to $FAKEWINETOP"
mkdir $FAKEWINETOP
cd $FAKEWINETOP
for i in /home/lenkne/shared/arc/server/arcgis/server/*;do ln -s $i . ;done
rm framework
mkdir framework
cd framework
for i in /home/lenkne/shared/arc/server/arcgis/server/framework/*;do ln -s $i . ;done
rm runtime
mkdir runtime
cd runtime
for i in /home/lenkne/shared/arc/server/arcgis/server/framework/runtime/*;do ln -s $i . ;done
cp -r /home/lenkne/shared/arc/server/arcgis/server/framework/runtime/.wine .
cd .wine
export DOTWINE=$(pwd)

cd $FAKEWINETOP
rm bin
mkdir bin
cd bin
for i in /home/lenkne/shared/arc/server/arcgis/server/bin/*;do ln -s $i .;done
cp -r /home/lenkne/shared/arc/server/arcgis/server/bin/.wine .


echo "Launcing script"
while [[ $MAXTRIES -gt 0 ]]; do 
    /home/lenkne/shared/arc/server/arcgis/server/tools/python /home/lenkne/shared/solar_scripts/batchSolarAnalyst.py 2>&1
    echo "$(hostname) - wine down again ($MAXTRIES tries left) -"
    sleep $(( ( RANDOM % 10 )  + 10 ))
    ((MAXTRIES--))
done

echo "$(hostname) I tried to start python/wine 100 times. I'm giving up and going home."
