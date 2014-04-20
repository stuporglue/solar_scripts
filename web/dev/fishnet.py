#!/usr/bin/env python
import sys,os

sys.path.insert(0, '../../steps_sql') # Add our steps_sql dir to our library path
import dbconn

print "Content-Type: text/html; charset=utf-8"
print 

q = """
SELECT state,AVG(time),COUNT(state)
FROM 
sa_fishnets 
GROUP BY state
"""

cur = dbconn.run_query(q)
obj = dbconn.cursor_to_object(cur,'state')

totalRecords = 0
for k in obj:
    totalRecords += obj[k]['count']

for x in range(-3,3):
    if not x in obj:
        obj[x] = {'count':0,'avg':0}


print """
<!DOCTYPE HTML>
<html>
<head>
<title>Spatial Analyst Fishnet Progress</title>
<style>
table
{
border-collapse:collapse;
}
table, th, td
{
border: 1px solid black;
}
</style>
</head>
<body>
<h1>Solar Analyst Progress</h1>

<h2>Current Status</h2>
<table>
<tr><th>Total Rows</th><td>""" + str(totalRecords) + """
<tr><th>Completed Rows</th><td>""" + str(obj[2]['count']) + """</td></tr>
<tr><th>Rows In Progress</th><td>""" + str(obj[1]['count']) + """</td></tr>
<tr><th>Failed Rows</th><td>""" + str(obj[-3]['count']) + """</td></tr>
<tr><th>Rows Left</th><td>""" + str(obj[0]['count']) + """
<tr><th>Percent Complete</th><td>""" + str(float(obj[2]['count']) / float(totalRecords) * 100.0) + """</td></tr>
<tr><th>Average time</th><td>""" + str(obj[2]['avg']) + """</td></tr>
</table>
"""

def timeLeft(timePer,totalLeft,instances):
    minutesleft = int(float(obj[0]['count']) * float(obj[2]['avg']) / 60.0 / float(x))
    totalminutes = minutesleft

    days = minutesleft/(60*24)
    hours = (minutesleft - days*24*60)/60
    minutes = (minutesleft - days*24*60 - hours*60)

    ret = "<tr><td>" + str(instances)+ "</td>"
    ret += "<td>" + str(totalminutes) + "</td>"
    ret += "<td>" + str(days) + "</td>"
    ret += "<td>" + str(hours) + "</td>"
    ret += "<td>" + str(minutes) + "</td></tr>"
    return ret

out = ""
for x in range(1,10):
    out += timeLeft(obj[0]['count'],obj[2]['avg'],x)

for x in range(10,100,10):
    out += timeLeft(obj[0]['count'],obj[2]['avg'],x)

for x in range(100,1001,100):
    out += timeLeft(obj[0]['count'],obj[2]['avg'],x)


print """
<h2>Projected Status</h2>
<table>
<tr><th>Number of concurrent processes</th>
<th>Total Minutes Left</th>
<th>Days Left</th>
<th>Hours Left</th>
<th>Minutes Left</th></tr>""" + out + """
</table>
</body>
</html>
"""
