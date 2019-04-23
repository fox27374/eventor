#!env/bin/python

from cfg import dklib

id_event = '0001'
query = dklib.get_sql_from_event(id_event)

# Create CSV
dklib.db_to_csv(id_event)

print "Content-type:text/html\r\n\r\n"
print '<html>'
print '<head>'
print '<title>AV Wattens</title>'
print '<link rel="stylesheet" href="eventor.css">'
print '</head>'
print '<body>'
print '<div class="wrapper">'
print '<div class="navbar">'
print '<a class="buttonDownload" href="files/file0001.csv" download="Jahreskarten.csv">Download CSV</a>'
print '</div>'
print dklib.db_to_html(id_event)
print '</div>'
print '</body>'
print '</html>'

