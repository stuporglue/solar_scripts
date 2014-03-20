# Continue fetching fishnet tiles that haven't been processed yet
# Fetch the list of lidar files for those tiles and process them

# DEMs fishnet squares have 4 states in the database: 
# -1 -- square has no intersecting lidar bboxes within 100m
# 0 -- available to process
# 1 -- reserved, but not complete
# 2 -- completed

import dbconn

buffersize  = 50

if len(sys.argv) != 2:
    print "Usage fishnet2blast.py <outputdir>"
    exit(-1)

outputdir   = sys.argv[1]

reserveQuery = " 
    UPDATE 
    dem_fishnets dem 
    SET state=1 
    WHERE 
    dem.id in (SELECT id FROM dem_fishnets WHERE state=0 LIMIT 1)
    RETURNING 
    id,
    ST_XMin(the_geom) as xmin,
    ST_YMin(the_geom) as ymin,
    ST_XMax(the_geom) as xmax,
    ST_YMax(the_geom) as ymax
"

lidarlist = "
    SELECT bbox.* FROM 
    dem_fishnets dem,
    lidar_bbox bbox
    WHERE dem.id=DEMID
    AND 
    ST_Intersects(ST_Buffer(dem.the_geom,100),bbox.the_geom)
"

completeQuery = "
    UPDATE 
    dem_fishnets dem
    SET state=2
    WHERE
    dem.id=DEMID
"

# Lidar is an array of lidar files to consider
# line is (xmin,ymin,xmax,ymax) for the output area
# buffersize is the buffer to apply for consideration
# outputdir is the directory where the files should be saved
def blast2dem(demid,lidar,line,buffersize,outputdir)

    line = linestr.strip().split(',')
    outputfile = outputdir + '\\' + '_'.join(line) + '.img'
    cmd = ['blast2dem']

    # Input tiles
    cmd.append('-i ' + ' '.join(lidar))

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
        sys.stdout.write("\t\t\t" + error)
        os.unlink(outputdir + "\\" + filename)
        return
    if returncode != 0:
        sys.stdout.write("\t\t\t" + output)
        os.unlink(outputdir + "\\" + filename)
        return

    # Remove empty files. Will happen where fishnet is off the map
    # 750703 -- 748kb files when they're solid black (also no results)
    if skipping.match(output) or int(os.stat(outputdir + "\\" + filename).st_size) == 750703:
        sys.stdout.write("\t\t\tNo data found, not saving tile.")
        os.unlink(outputfile)
        return

res = dbconn.run_query(reserveQuery)
while len(res) > 0:
    for row in res:
        os.stdout.write("\nRunning blast2dem for row " + str(row['id']))

        lidars = []
        lidares = dbconn.run_query(lidarlist.replace("DEMID",str(row['id'])))
        for lidar in lidares:
            lidars.append(lidar['lasfile'])

        blast2dem(row['id'],lidars,(row['xmin'],row['ymin'],row['xmax'],row['ymax']),buffersize,outputdir)
        dbconn.run_query(completeQuery.replace("DEMID",str(row['id'])))

    res = dbconn.run_query(reserveQuery)
