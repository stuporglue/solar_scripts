# coding=UTF-8
# Run blast2dem on every square in a fishnet
# with all laz files as input so that output
# is buffered and you don't have border line
# artifacts

import sys,glob,subprocess,re,os

if len(sys.argv) != 4:
    print "Usage fishnet2blast.py <input directory> <outputdir> <fishnet csv file>"
    print len(sys.argv)
    exit(-1)

basepath    = sys.argv[1]
outputdir   = sys.argv[2]
fishnetfile = sys.argv[3]
buffersize  = 50

with open(fishnetfile,'r') as f:
    content = f.read().split("\n")

################ Running our functions on input data
globs = []
for curdir in glob.glob(basepath + '\\q*'):
    globs.append(curdir + '\\laz\\*.laz')

skipping = re.compile('.*bounding box. skipping.*',re.DOTALL)
for linestr in content:

    line = linestr.strip().split(',')
    outputfile = outputdir + '\\' + '_'.join(line) + '.img'
    cmd = ['blast2dem']

    # Input tiles
    cmd.append('-i ' + ' '.join(globs))

    # Spatial Filtering 
    # This defines the buffered area used for calcultions
    cmd.append('-inside ' + str(int(line[0]) - buffersize) + ' ' + str(int(line[1]) - buffersize) + ' ' + str(int(line[2]) + buffersize) + ' ' + str(int(line[3]) + buffersize))
    # This defines the output lower-left corner
    cmd.append('-ll ' + line[0] + ' ' + line[1])
    # This defines the output tile's height and width
    cmd.append('-ncols ' + str(int(line[2]) - int(line[0])))
    cmd.append('-nrows ' + str(int(line[3]) - int(line[1])))

    # Data Filtering 
    cmd.append('-first_only')
    cmd.append('-elevation')

    # Output parameters
    cmd.append('-v')
    cmd.append('-merged')
    cmd.append('-oimg')
    cmd.append('-o ' + '_'.join(line) + '.img')
    cmd.append('-odir ' + outputdir)

    command = ' '.join(cmd)

    #print "-----------------------------------------"
    print command

    # Check output
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    output,error = process.communicate()
    returncode = process.poll()

    #print "RETCODE: " + str(returncode)
    #print "ERROR: " + str(error)
    #print "OUTPUT: " + str(output)

    # Print errors
    if error != None:
        print error
    if returncode != 0:
        print output

    # Remove empty files. Will happen where fishnet is off the map
    if skipping.match(output):
        print "No data found"
        os.unlink(outputfile)



