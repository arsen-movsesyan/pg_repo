#!/usr/local/bin/python -B

import argparse
import sys
import re
import settings
import psycopg2

parser = argparse.ArgumentParser(description='Database changes and updates tracking system')

parser.add_argument('-r',action='store_true',dest='dry_run',default=False,help="Show updates and exit")
parser.add_argument('-i','--install',action='store_true',default=False,help="Install application and go to dry_run mode")
parser.add_argument('-s',nargs=1,choices=['file','SQLite'],default='file',dest='source',
    help="Source for updates. SQLite is not supported currently")
parser.add_argument('-v','--verbose',action='store_true',default=False,help="Show additional info on terminal")
parser.add_argument('-l','--last',dest='last_applied',action='store_true',default=False,
    help="Show last applied update number and exit")

args=parser.parse_args()

class UpdSource():

    def __init__(self,in_source):
	self.upd_dict=dict()
	self.source=in_source
	self.src_handler=None

    def _define_updates(self):
	if self.source=='file':
	    import updates
#		for upd in dir(incremetal):
		    


#    def _iterate(self):
#	if not self.src_handler:
#	    if self._define_handler():
#		for line in self.src_handler


class DbState():

    def __init__(self,in_db_conn):
	self.db_conn=in_db_conn
	self.last_applied=None
	self.installed=-1
#	self.check_installed()

    def __del__(self):
	if not self.db_conn.closed:
	    self.db_conn.close()

    def get_last_applied(self):
	if not self.last_applied:
	    cur=self.db_conn.cursor()
	    try:
		cur.execute("SELECT COALESCE(MAX(update_number),0) FROM db_update")
	    except Exception as e:
		print "Error! Cannot get last applied update! {0}".format(e.pgerror)
		return False
	    self.last_applied=cur.fetchone()[0]
	    cur.close()
	return self.last_applied

    def _check_installed(self):
	cur=self.db_conn.cursor()
	try:
	    cur.execute("SELECT COUNT(1) FROM pg_class WHERE relname='db_update' AND relkind='r'")
	except Exception as e:
	    print "ERROR! Cannot determine installed! {0}".format(e.pgerror)
	    return False
	self.installed=cur.fetchone()[0]
	return True

    def install(self):
	cur=self.db_conn.cursor()
	try:
	    cur.execute("""CREATE table db_update(
update_number integer NOT NULL PRIMARY KEY,
update_content text NOT NULL,
update_time timestamp with time zone NOT NULL DEFAULT now())""")
	except Exception as e:
	    print "ERROR! Cannot create db_update table!{0}".format(e.pgerror)
	    return False
	else:
	    self.db_conn.commit()
	    print "Application successfully installed"
	    return True

    def get_installed(self):
	if self.installed == -1:
	    self._check_installed()
	return self.installed

#########################################################################
if args.install:
    args.dry_run=True

try:
    conn=psycopg2.connect(settings.custom_dsn('db_handler_1'))
except Exception as e:
    print "ERROR! Cannot connect to database {0}".format(e)
    sys.exit(1)


db_st=DbState(conn)

installed=db_st.get_installed()

if installed == 0:
    install=db_st.install()
    if not install:
	conn.close()
	sys.exit(1)
elif installed == 1:
    if args.install:
	print "Application already installed"
elif installed == -1:
    conn.close()
    sys.exit(1)


last_applied=db_st.get_last_applied()

if args.last_applied:
    if last_applied == 0:
	print "No updates applied"
    else:
	print "Last applied update: upd_{0}".format(last_applied)
    conn.close()
    sys.exit()


