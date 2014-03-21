# Continue fetching fishnet tiles that haven't been processed yet
# Fetch the list of lidar files for those tiles and process them

# DEM states
# -3 -- errors encountered
# -2 -- areas calculated to have no tiles within 100m
# -1 -- square has no intersecting lidar bboxes within 100m
# 0 -- available to process
# 1 -- reserved, but not complete
# 2 -- completed

import dbconn,sys,os,subprocess,re,tempfile

buffersize  = 50

if len(sys.argv) != 2:
    print "Usage fishnet2blast.py <outputdir>"
    exit(-1)

outputdir   = sys.argv[1]

# Radiate outwards from Blegen Hall
reserveQuery = """
    UPDATE dem_fishnets dem 
    SET state=1 
    WHERE dem.id in (
        SELECT id FROM dem_fishnets WHERE state=0 
        ORDER BY ST_Distance(the_geom,ST_SetSrid(ST_MakePoint(480815.0,4979852.6),32615))
        LIMIT 1
    ) 
    RETURNING 
    id, 
    ST_XMin(the_geom) as xmin, 
    ST_YMin(the_geom) as ymin, 
    ST_XMax(the_geom) as xmax, 
    ST_YMax(the_geom) as ymax
"""

lidarlist = """
    SELECT bbox.* FROM 
    dem_fishnets dem,
    lidar_bbox bbox
    WHERE dem.id=DEMID
    AND 
    ST_Intersects(ST_Buffer(dem.the_geom,100),bbox.the_geom)
"""

completeQuery = """
    UPDATE 
    dem_fishnets dem
    SET state=NEWSTATE
    WHERE
    dem.id=DEMID
"""

# demid is the database ID of the dem fishnet square we're working on
# lidarlist is a text file with a list of lidar files to use. This is needed because the command line gets too long for Powershell or blast2dem (not sure which)
# line is (xmin,ymin,xmax,ymax) for the output area
# buffersize is the buffer to apply for consideration
# outputdir is the directory where the files should be saved
def blast2dem(demid,lidarlist,line,buffersize,outputdir):

    outputfile = outputdir + '\\' + '_'.join(line) + '.img'
    cmd = ['blast2dem']

    # Input tiles
    cmd.append('-lof ' + lidarlist)

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
    filename = str(demid) + '.img'
    cmd.append('-o ' + filename)
    cmd.append('-odir ' + outputdir)

    command = ' '.join(cmd)

    # print "-----------------------------------------"
    # print command
    # return 


    # Check output
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        output,error = process.communicate()
        returncode = process.poll()
    except:
        e = sys.exc_info()[0]
        sys.stdout.write("\t\t\t" + str(e))
        print "\n\t\t" + command 
        if os.path.isfile(outputdir + "\\" + filename):
            os.unlink(outputdir + "\\" + filename)
        return False

    #print "RETCODE: " + str(returncode)
    #print "ERROR: " + str(error)
    #print "OUTPUT: " + str(output)

    # Print errors
    if error != None:
        sys.stdout.write("\t\t\t" + error)
        print "\n\t\t" + command 
        if os.path.isfile(outputdir + "\\" + filename):
            os.unlink(outputdir + "\\" + filename)
        return False
    if returncode != 0:
        sys.stdout.write("\t\t\t" + output)
        print "\n\t\t" + command 
        if os.path.isfile(outputdir + "\\" + filename):
            os.unlink(outputdir + "\\" + filename)
        return False

    # Remove empty files. Will happen where fishnet is off the map
    # 750703 -- 748kb files when they're solid black (also no results)
    if re.match('.*bounding box. skipping.*',output,re.DOTALL) or int(os.stat(outputdir + "\\" + filename).st_size) == 750703:
        sys.stdout.write("\t\t\tNo data found, not saving tile.")
        os.unlink(outputfile)
        return True

    return True

res = dbconn.run_query(reserveQuery).fetchall()
while len(res) > 0:
    for row in res:
        sys.stdout.write("\nRunning blast2dem for row " + str(row['id']) + "\t\t\t")

        tmp = tempfile.NamedTemporaryFile(delete=False)
        lidares = dbconn.run_query(lidarlist.replace("DEMID",str(row['id']))).fetchall()
        for lidar in lidares:
            tmp.write(lidar['lasfile'] + "\n")
        tmp.close()

        blasted = blast2dem(demid=row['id'],lidarlist=tmp.name,line=[str(int(row['xmin'])),str(int(row['ymin'])),str(int(row['xmax'])),str(int(row['ymax']))],buffersize=buffersize,outputdir=outputdir)

        os.unlink(tmp.name)

        if blasted:
            print "DONE!"
            dbconn.run_query(completeQuery.replace("DEMID",str(row['id'])).replace('NEWSTATE','2'))
        else:
            print "Error"
            dbconn.run_query(completeQuery.replace("DEMID",str(row['id'])).replace('NEWSTATE','-3'))

    res = dbconn.run_query(reserveQuery).fetchall()
