pg_repo
=======

Simple database changes and upgrades tracking system

Installation:

First edit "settings.py" file modify DATABASE['db_handler_1'] parameters to connect to your database

Run "python db_update.py -h" for help
Run "python db_update.py -i" for installation


Incremental update format.

File "updates must contain all incremental updates in following format:

    upd_<update_number>="<DDL statement in quotes here>"

Example:

    upd_1="CREATE TABLE foo (id INTEGER PRIMARY KEY, field text)"
    upd_2="ALTER TABLE foo ADD COLUMN when TIMESTAMPTZ DEFAULT now()"

Numbers must be sequentially incremented.
Empty lines are ignored.
