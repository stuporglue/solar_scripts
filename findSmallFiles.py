import os
import glob

os.chdir('F:\\SolarResourceData\\Final_SRR\\')

for dir in glob.glob('*'):
    if os.path.isdir(dir):
        updates = []
        for file in glob.glob(dir + "\\*.img"):
            if os.path.getsize(file) <= 1375231:
                idno = file.replace(dir,'').replace('\\SRR_','').replace('.img','')
                if idno != '\\':
                    updates.append(idno)
        print "UPDATE sa_fishnets SET state=0 WHERE id IN (" + ','.join(updates) + ");"
