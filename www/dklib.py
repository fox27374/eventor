#!../env/bin/python

import mysql.connector
import csv
import json
import os

def get_config():
    config = {}
    configfile = 'cfg/config.json'
    with open (configfile, 'r') as c:
        config = json.load(c)
    return config

def create_dbh():
    config = get_config()
    dbh = mysql.connector.connect(
        host = config['host'],
        user = config['user'],
        passwd = config['passwd'],
        database = config['database'])
    return dbh

def get_mysql_count(id_event):
    sql = 'SELECT COUNT(*) FROM t' + id_event + ';'
    cnx = create_dbh()
    cursor = cnx.cursor()
    cursor.execute(sql)
    count = cursor.fetchone()
    return count[0]

def query_mysql(id_event):
    sql = get_sql_from_event(id_event)
    cnx = create_dbh()
    cursor = cnx.cursor()
    cursor.execute(sql)
    # Get header and rows
    header = [i[0] for i in cursor.description]
    rows = [list(i) for i in cursor.fetchall()]
    # Append header to rows
    rows.insert(0,header)
    cursor.close()
    cnx.close()
    return rows

def db_to_html(id_event):
    data = query_mysql(id_event)
    htable=u'<div class="table">'
    # Create header
    header = u'<div class="row header blue">'
    for item in data[0]:
        header += u'<div class="cell">' + unicode(item) + u'</div>'
    header += u'</div>'
    htable += header

    del data[0]
    for row in data:
        newrow = u'<div class="row">'
        newrow = newrow + ''.join([u'<div class="cell">' + unicode(x).encode('ascii', 'xmlcharrefreplace') + u'</div>' for x in row])
        newrow += '</div>'
        htable+= newrow
    htable += '</div>'
    return htable

def db_to_csv(id_event):
    csvfile = 'files/file{}.csv'.format(id_event)
    data = query_mysql(id_event)
    #fp = open(csvfile, 'w')
    with open(csvfile, 'w') as fp:
        myFile = csv.writer(fp)
        for row in data:
            enc = [unicode(x).encode('UTF-8') for x in row]
            myFile.writerow(enc)
    fp.close()

def sql_html(query):
	return nlist_to_html(query_mysql(query))

def get_sql_from_event(id_event):
    event_query_map={}
    event_query_map['0001'] = "SELECT t_date as Datum, t_title as Anrede, t_name as Vorname, t_surname as Nachname, t_birth as Geburtstag, t_ebname as EBVorname, t_ebsurname as EBNachname, t_street as Strasse, t_number as Hausnummer, t_zip as PLZ, t_city as Stadt, t_section as Sektion, t_membernumber as AVNummer, t_guest as Gast, t_phone as Telefonnummer, t_mail as Email, t_membership as Jahreskarte, t_family as Familie FROM t0001 ORDER BY Datum desc;"

    sql = event_query_map[id_event]

    return sql

