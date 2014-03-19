#
# blast2dem.py
# blast all MN Lidar to DEM
# walz0053@umn.edu
#

import sys, os, subprocess, glob
from distutils.spawn import *


################ Usage check and argument assigning
if len(sys.argv) != 3:
    print "Usage: blast2dem.py <input directory> <output directory>"
    print "The intput directory should have the q**** directories in it, eg. c:\base\path\to\q***"
    print "Contents in the output directory will be overwritten"
    exit(-1)
else:
    basepath = sys.argv[1]
    outputdir = sys.argv[2]

if find_executable('blast2dem') == None:
    print "Please make sure that blast2dem.exe is in your PATH environment"
    exit(-1)

if not os.path.isdir(basepath):
    print "Input directory must be a directory and exist"
    exit(-1)

if not os.path.isdir(outputdir):
    print "Output directory must be a directory and exist"
    exit(-1)

################ Function definitions

def check_output(command,console):
    if console == True:
        process = subprocess.Popen(command)
    else:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    output,error = process.communicate()
    returncode = process.poll()
    return returncode,output 

def blast2dem(inlaz,qnum):
    ### create the command string for blast2dem.exe
    command = ["blast2dem"] 

    ### use '-verbose' option
    command.append("-v")

    ### add input LiDAR
    command.append('-i')
    ##wildcards = sys.argv[c+1].split()
    ##for wildcard in wildcards:
    ##    command.append("-i")
    ##    command.append('"' + sys.argv[c] + "\\" + wildcard + '"')
    #command.append('"' + "C:\\lidar_data\\hennepin\\laz\\test_blast\\q1110\\1110*.laz" + '"')
    command.append('"' + inlaz + '"')

    ### options
    command.append("-merged")
    command.append("-first_only")
    command.append("-elevation")
    command.append("-kill")
    command.append("50")
                   
    ##command.append("-drop_return")
    ##command.append("0")
    ##command.append("1")
    ##command.append("7")
    ##command.append("12")

    command.append("-oimg")

    ### maybe an output file name was selected
    command.append("-o")
    command.append('"'+ qnum +'.img"')

    ### maybe an output directory was selected
    command.append("-odir")
    command.append('"' + outputdir + '"')


    ### report command string
    print "LAStools command line:"
    command_length = len(command)
    command_string = str(command[0])
    command[0] = command[0].strip('"')
    for i in range(1, command_length):
        command_string = command_string + " " + str(command[i])
        command[i] = command[i].strip('"')
    print command_string

    print "Would run: " + command_string

    #### run command
    #returncode,output = check_output(command, False)

    #### report output of blast2dem
    #print str(output)

    #if returncode != 0:
    #    print "Error. blast2dem failed."
    #    sys.exit(1)

    #print "Success. blast2dem done."


################ Running our functions on input data
f = []
for curdir in glob.glob(basepath + '\\q*'):
    lazfiles = glob.glob(curdir + '\\laz\\*.laz')

    print 'Processing ' + str(len(lazfiles)) + ' laz files in ' + curdir + '\\laz\\'
    qnum = os.path.basename(os.path.realpath(curdir))
    blast2dem(curdir + '\\laz\\*.laz',qnum)
