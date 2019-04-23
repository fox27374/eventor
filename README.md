Eventor
=======

Tool to handle event registrations. Data is sent by a form via email to a mailserver
where the **process_mail.py** script saves a copy of the mail and extracts
the data and writes it into a mysql database.

This data can then be read by the **index.py** file located in the webroot
if a webserver.
