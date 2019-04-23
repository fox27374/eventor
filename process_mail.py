#!/usr/bin/python

import sys
import re
import os
import modules
import datetime
import random

# Variable declaration
path = '/home/dk/'
maildir = path + 'mails/'
datafile = path + 'data.csv'
tmpfile = path + 'tmp.msg'
subject = ''
name = ''
surname = ''


# Write message to tmp file
tmp = open(tmpfile, 'a')
for line in sys.stdin:
    if re.search(r'^Subject: ', line):
        subject = line[(line.find(':')+2):(len(line))].strip()
    if re.search(r'^Vorname: ', line):
        name = line[(line.find(':')+2):(len(line))].strip()
    if re.search(r'^Nachname: ', line):
        surname = line[(line.find(':')+2):(len(line))].strip()
    tmp.write(line)
tmp.close()


# Copy file to maildir
msgfile = maildir + str(datetime.date.today()) + '_' + subject + '_' + name + '_' + surname + '.msg'
if os.path.isfile(msgfile):
    msgfile = maildir + str(datetime.date.today()) + '_' + subject + '_' + name + '_' + surname + str(random.randint(1,10)) + '.msg'

cmd = 'cp {} {}'.format(tmpfile, msgfile)
os.system(cmd)

        
# Write data to DB based on subject
if '0001' in subject:
    modules.write_0001_db(modules.parse_0001(tmpfile))

# Delete tmpfile
rmfile = 'rm {}'.format(tmpfile)
os.system(rmfile)
