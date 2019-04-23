#!/usr/bin/python

import modules

def commit_sql(sql):
    # Get DB handler
    dbh = modules.create_dbh()

    # Write into DB
    dbc = dbh.cursor()
    dbc.execute(sql)
    dbh.commit()

def create_table_events():
    sql = 'CREATE TABLE IF NOT EXISTS events (t_id CHAR(4), t_name VARCHAR(35), t_status CHAR(10), PRIMARY KEY (t_id))'
    commit_sql(sql)

def create_table_0001():
    # Prepare SQL query
    sql = 'CREATE TABLE IF NOT EXISTS t0001 (t_id INT UNSIGNED AUTO_INCREMENT, t_date DATETIME, t_title CHAR(4), t_name CHAR(25), t_surname CHAR(25), t_birth DATE, t_ebname CHAR(25), t_ebsurname CHAR(25), t_street CHAR(50), t_number CHAR(10), t_zip SMALLINT UNSIGNED, t_city CHAR(50), t_section CHAR(50), t_membernumber CHAR(10), t_guest CHAR(3), t_phone CHAR(20), t_mail CHAR(30), t_membership CHAR(50), t_family VARCHAR(200), PRIMARY KEY (t_id))'

    commit_sql(sql)

#create_table_events()
create_table_0001()


