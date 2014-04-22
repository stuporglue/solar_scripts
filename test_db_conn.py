# Test if the database connection is working

import dbconn

res = dbconn.run_query("SELECT true as working").fetchall()

print str(res)
