# coding=UTF-8
# Run blast2dem on every square in a fishnet
# with all laz files as input so that output
# is buffered and you don't have border line
# artifacts

import sys,glob,subprocess,re,os

if len(sys.argv) != 4:
    print "Usage fishnet2blast.py <input directory> <outputdir> <fishnet csv file>"
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
total = len(content) - 1
for idx,linestr in enumerate(content[1:]):

    print ""
    sys.stdout.write(str(int(idx/total)) + "% done, current tile is (" + str(idx) + "/" +str(total) + "), (" + linestr + ")")

    line = linestr.strip().split(',')
    outputfile = outputdir + '\\' + '_'.join(line) + '.img'
    cmd = ['blast2dem']

    # Input tiles
    cmd.append('-i ' + ' '.join(globs))

    # Processing parameters
    cmd.append('-merged')
    cmd.append('-step 1')

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
    cmd.append('-drop_class 1 2 3')

    # Output parameters
    cmd.append('-v')
    cmd.append('-oimg')
    filename = '_'.join(line) + '.img'
    cmd.append('-o ' + filename)
    cmd.append('-odir ' + outputdir)

    command = ' '.join(cmd)

    #print "-----------------------------------------"
    #print command

    if os.path.isfile(outputdir + "\\" + filename):
        sys.stdout.write("\t\t\tAlready Exists. Not Re-generating")
        continue

    # Check output
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    output,error = process.communicate()
    returncode = process.poll()

    #print "RETCODE: " + str(returncode)
    #print "ERROR: " + str(error)
    #print "OUTPUT: " + str(output)

    # Print errors
    if error != None:
        sys.stdout.write("\t\t\t" + error)
        os.unlink(outputdir + "\\" + filename)
        continue
    if returncode != 0:
        sys.stdout.write("\t\t\t" + output)
        os.unlink(outputdir + "\\" + filename)
        continue

    # Remove empty files. Will happen where fishnet is off the map
    # 750703 -- 748kb files when they're solid black (also no results)
    if skipping.match(output) or int(os.stat(outputdir + "\\" + filename).st_size) == 750703:
        sys.stdout.write("\t\t\tNo data found, not saving tile.")
        os.unlink(outputfile)
        continue

    sys.stdout.write("\t\t\tDONE!")
