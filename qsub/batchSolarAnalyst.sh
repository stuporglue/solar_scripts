#!/bin/bash

# Clone the neccessary bits from an arcgis server install so that we can run on a supercomputer

#######################################################################################
#
# Configuration options
#
MAXTRIES=100

# Any logmsg with a level under DEBUG_LEVEl will be printed
# Level 0 -- normal messages
# Level 1 -- debug messages
# Level 2 -- very verbose
DEBUG_LEVEL=2

REALARCINSTALL="/home/lenkne/shared/arc/server/arcgis/server"
REALDATADIR="/home/lenkne/shared"

# Make a fake Wine directory for each individual job
FAKEWINETOP="/scratch/lenkne/fakeWine_$(hostname)_$PBS_VNODENUM"
FAKEDATADIR="/scratch/lenkne/data"
#######################################################################################





#######################################################################################
#
# Initial setup and function declarations
#
# Make the base data dir now so that we can use a sub directory creation as a mutex later
mkdir -p $FAKEDATADIR

export PATH=$REALARCINSTALL/tools/:$PATH
export LD_LIBRARY_PATH=$REALDATADIR/arc/libs:$LD_LIBRARY_PATH
export LOGNAME=$(stat -c %U $REALARCINSTALL)
export WINEDEBUG="-all"
export DOTWINE=$REALARCINSTALL/framework/runtime/.wine

# Make a symlink clone of a directory
# fakedirs(/home/lenkne/shared/arc/server/rcgis/server/,/scratch/lenkne/fakeWine_host_jobno)
# Assumes that destdir exists and is a directory or that it doesn't exist yet (it can't be a symlink)
function fakedirs {
    sourcedr=$1
    destdir=$2

    logmsg "Making fake $destdir from  $sourcedr" 1

    # Make the dest dir if it doesn't exist
    if [[ -h $destdir ]];then
        rm -f $destdir
    fi
    mkdir -p $destdir

    # Switch to the dest dir
    pushd $destdir >/dev/null

    # For every file in the sourcedir, symlink to it in the dest dir
    for i in $sourcedr/*;do
        if [[ ! -e $(basename $i) ]];then
            logmsg "Linking $i to $(pwd)/$(basename $i)" 2
            ln -s $i
        fi
    done

    # Change back to the directory we were in
    popd >/dev/null
}

# Log messages if they are within the debug level
function logmsg {
    if [[ "x$2" = "x" ]];then
        level=0
    else
        level=$2
    fi
    
    if [[ $DEBUG_LEVEL -gt $level ]];then
        echo $1
    fi
}



#######################################################################################
#
# Every process gets its own Wine directory. One wine directory per core per node
#

starttime=$(date +%s)

logmsg "$(hostname) Cloning Wine" 1
fakedirs $REALARCINSTALL $FAKEWINETOP
fakedirs $REALARCINSTALL/bin $FAKEWINETOP/bin
fakedirs $REALARCINSTALL/framework $FAKEWINETOP/framework
fakedirs $REALARCINSTALL/framework/runtime $FAKEWINETOP/framework/runtime
 
# Copy the actual wine directory now
logmsg "$(hostname) copying actual .wine dir #1" 1
if [[ -h $FAKEWINETOP/framework/runtime/.wine ]];then rm .wine;fi
logmsg "rsync -rl $REALARCINSTALL/framework/runtime/.wine/ $FAKEWINETOP/framework/runtime/.wine/" 1
rsync -rl $REALARCINSTALL/framework/runtime/.wine/ $FAKEWINETOP/framework/runtime/.wine/

logmsg "$(hostname) copying actual .wine dir #2" 1
if [[ -h $FAKEWINETOP/bin/.wine ]];then rm .wine; fi
logmsg "rsync -rl $REALARCINSTALL/bin/.wine/ $FAKEWINETOP/bin/.wine/" 1
rsync -rl $REALARCINSTALL/bin/.wine/ $FAKEWINETOP/bin/.wine/

endtime=$(date +%s)
logmsg "It took $((endtime - starttime)) seconds to clone wine" 1


#######################################################################################






#######################################################################################
#
# Every node gets its own clone of the GeoDatabase. All cores/jobs on a node will share the copied GDB
#

# 8 instances of this script will be running and we only want one of them to clone
# the GDB to the local node. We're going to use mkdir to acquire and release 
# a file lock

# Only one instance of the script should succeed in running mkdir
# Possibly zero instances if we run a second batch job and end up on the same node as we were on before

# We're going to use mkdir to acquire a mutex on the directory
if mkdir "$FAKEDATADIR/ready_for_$PBS_JOBID" 2>/dev/null; then
    starttime=$(date +%s)
    logmsg "$PBS_NODENUM/$PBS_VNODENUM got the lock on $(hostname)" 1
    mkdir -p $FAKEDATADIR/MinnesotaLiDAR_DSM
    echo "rsync -rl $REALDATADIR/MinnesotaLiDAR_DSM/MN_DEM.gdb/ $FAKEDATADIR/MinnesotaLiDAR_DSM/MN_DEM.gdb/" 1
    rsync -rl $REALDATADIR/MinnesotaLiDAR_DSM/MN_DEM.gdb/ $FAKEDATADIR/MinnesotaLiDAR_DSM/MN_DEM.gdb/
    fakedirs $REALDATADIR/MinnesotaLiDAR_DSM $FAKEDATADIR/MinnesotaLiDAR_DSM
    mkdir "$FAKEDATADIR/ready_for_$PBS_JOBID"
    endtime=$(date +%s)
    logmsg "It took $((endtime - starttime)) seconds to clone the gdb" 1
else
    # The scripts that didn't mkdir will loop waiting for ready_to_use to exist
    logmsg "$PBS_NODENUM/$PBS_VNODENUM waiting for lock release on $(hostname)" 1
    while [[ ! -d $FAKEDATADIR/ready_for_$PBS_JOBID ]];do
        sleep 5
    done
fi
#######################################################################################





#######################################################################################
#
# Finally, we launch the actual job. Since Wine is still a little crashy, we're going to try to start the job 100 times
#
echo "Launching script on $(hostname)"
while [[ $MAXTRIES -gt 0 ]]; do 
    $REALARCINSTALL/tools/python $REALDATADIR/solar_scripts/batchSolarAnalyst.py 2>&1
    logmsg "$(hostname) - wine down again ($MAXTRIES tries left) -" 0
    sleep $(( ( RANDOM % 10 )  + 10 ))
    ((MAXTRIES--))
done

logmsg "$(hostname) I tried to start python/wine 100 times. I'm giving up and going home." 0
