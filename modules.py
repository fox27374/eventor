import re
import csv
import time
import datetime
import os
import json
import mysql.connector

def get_config():
    config = {}
    configfile = 'config.json'
    with open (configfile, 'r') as c:
        config = json.load(c)
    return config

def create_dbh():
    config = get_config()
    dbh = mysql.connector.connect(
        host = config['host'],
        user = config['username'],
        passwd = config['password'],
        database = config['db'])

    return dbh

def parse_0001(tmpfile):

    data = {}
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    data['date'] = timestamp

    # Initialise optional values
    data['ebname'] = 'NA'
    data['ebsurname'] = 'NA'
    
    msg = open(tmpfile, "r")
    for line in msg:
        line = line.strip()
        if re.search(r'^Anrede: ', line):
            data['title'] = line[(line.find(':')+2):(len(line))]
        if re.search(r'^Vorname: ', line):
            data['name'] = line[(line.find(':')+2):(len(line))]
        if re.search(r'^Nachname: ', line):
            data['surname'] = line[(line.find(':')+2):(len(line))]
        if re.search(r'^Geburtsdatum: ', line):
            data['birth'] = line[(line.find(':')+2):(len(line))]
        if re.search(r'^EB.Vorname: ', line):
            data['ebname'] = line[(line.find(':')+2):(len(line))]
        if re.search(r'^EB.Nachname: ', line):
            data['ebsurname'] = line[(line.find(':')+2):(len(line))]
        if re.search(r'^Stra', line):
            data['street'] = line[(line.find(':')+2):(len(line))]
        if re.search(r'^Nummer', line):
            data['number'] = line[(line.find(':')+2):(len(line))]
        if re.search(r'^Postleitzahl: ', line):
            data['zip'] = line[(line.find(':')+2):(len(line))]
        if re.search(r'^Ort: ', line):
            data['city'] = line[(line.find(':')+2):(len(line))]
        if re.search(r'^AV.Mitgliedschaft: ', line):
            data['section'] = line[(line.find(':')+2):(len(line))]
        if re.search(r'^AV.Mitgliedsnummer', line):
            data['membernumber'] = line[(line.find(':')+2):(len(line))]
        if re.search(r'^Gastmitgliedschaft', line):
            data['guest'] = line[(line.find(':')+2):(len(line))]
        if re.search(r'^Mobilnummer: ', line):
            data['phone'] = line[(line.find(':')+2):(len(line))]
        if re.search(r'^E-Mail: ', line):
            data['mail'] = line[(line.find(':')+2):(len(line))]
        if re.search(r'^Jahreskarte', line):
            data['membership'] = line[(line.find(':')+2):(len(line))]
        if re.search(r'^Familienmitglieder:', line):
            data['family'] = line[(line.find(':')+2):(len(line))]

    # Check data and modify values
    if 'Familienkarte' not in data['membership']: data['family'] = 'NA'
    data['guest'] = 'Yes' if 'Ja' in data['guest'] else 'No'
    data['section'] = 'Wattens' if 'Wattens' in data['section'] else 'Other'
    data['birth'] = datetime.datetime.strptime(data['birth'], '%d.%m.%Y')
    data['birth'] = datetime.datetime.date(data['birth'])

    return data


def write_0001_db(data):
    # Prepare SQL query
    sql = 'INSERT INTO t0001 (t_date, t_title, t_name, t_surname, t_birth, t_ebname, t_ebsurname, t_street, t_number, t_zip, t_city, t_section, t_membernumber, t_guest, t_phone, t_mail, t_membership, t_family) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    # Prepare variables
    values = (data['date'], data['title'], data['name'], data['surname'], data['birth'], data['ebname'], data['ebname'], data['street'], data['number'], data['zip'], data['city'], data['section'], data['membernumber'], data['guest'], data['phone'], data['mail'], data['membership'], data['family'])

    # Get DB handler
    dbh = create_dbh()

    # Write into DB
    dbc = dbh.cursor()
    dbc.execute(sql, values)
    dbh.commit()


def create_0001_html():
    table = 't0001'
    


def write_001_csv(data, datafile):
    csv_data = []
    csv_data.append(dict(data))

    # Create CSV
    fileempty = True
    if os.path.isfile(datafile):
        fileempty = os.stat(datafile).st_size == 0

    with open(datafile, mode='a') as csvfile:
        #fieldnames = ['Datum', 'Anrede', 'Vorname', 'Nachname', 'Geburtsdatum', 'AV', 'Telefon', 'EMail']
        fieldnames = ['date', 'title', 'name', 'surname', 'birth', 'ebname', 'ebsurname', 'street', 'number', 'zip', 'city', 'section', 'membernumber', 'guest', 'phone', 'mail', 'membership', 'family']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if fileempty:
            writer.writeheader()
        for info in csv_data:
            writer.writerow(info)

