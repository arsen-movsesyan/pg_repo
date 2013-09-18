TIME_ZONE = 'PST8PDT'
LANGUAGE_CODE = 'en-us'
APPLICATION_NAME= 'pg_repo'

DATABASE = {
    'db_handler_1': {
	'DBNAME': 'test_work',
	'USER': 'postgres',
	'PASSWORD': '',
	'HOST': 'localhost',
	'PORT': '5432',
	'SSLMODE': 'prefer',
    },
}


##############################################
### !!! Do not modify below this point !!! ###
##############################################

def custom_dsn(db_handler):
    for handler in DATABASE:
	if handler == db_handler:
	    portion=DATABASE[handler]
	    dbname=portion['DBNAME']
	    host=portion['HOST']
	    port=portion['PORT']
	    user=portion['USER']
	    password=portion['PASSWORD']
	    sslmode=portion['SSLMODE']
	    return "host="+host+" dbname="+dbname+" port="+port+" user="+user+" password="+password+" sslmode="+sslmode
