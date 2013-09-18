#!/usr/bin/env -S python -B

import psycopg2
import incremental
import re
import sys

db_conn=psycopg2.connect("host=localhost dbname=mobile_app user=postgres")
#db_conn.autocommit=True

cur=db_conn.cursor()

dry_run=False
if len(sys.argv) >= 2:
    if sys.argv[1] == '-d':
	dry_run=True


cur.execute("SELECT COALESCE(MAX(update_number),0) FROM db_update")
max_applied=cur.fetchone()[0]

#print max_applied

cur.close()

new_updates=[]

for upd in dir(incremental):
    if re.match("upd_\d",upd):
	if int(upd[4:]) > int(max_applied):
	    new_updates.append(upd[4:])
#	    print upd[4:]


for new_upd in sorted(new_updates):
    upd_number=new_upd
    upd_content=eval('incremental.upd_'+new_upd)
    cur=db_conn.cursor()
    query=cur.mogrify(upd_content)
    if dry_run:
	print query
    else:
	try:
	    cur.execute(query)
	except Exception as e:
	    print "Problem with query in upd_{0}\n{1}".format(upd_number,e.pgerror)
	    cur.close()
	    db_conn.close()
	    sys.exit(1)
	else:
	    cur.execute("INSERT INTO db_update(update_number,update_content) VALUES (%s,%s)",(upd_number,upd_content))
	db_conn.commit()
    cur.close()

db_conn.close()


