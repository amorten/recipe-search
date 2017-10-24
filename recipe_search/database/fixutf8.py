#!/usr/bin/python

import MySQLdb

from html2utf8 import html2utf8



print "Connecting to MySQL"
db = MySQLdb.connect (host = "localhost",
                        user = "root",
                        passwd = "tpofofntsff",
                        db = "recipesniffer-prod")

print "Creating cursor"
cursor = db.cursor(MySQLdb.cursors.DictCursor)

print "Executing select statement"
cursor.execute ("""select rec_id,ingred_text,
                   proced_text,html_title,rec_name 
                   from fixcopy""")
rows = cursor.fetchall()
newrow = {}
print "Beginning loop"
for row in rows:
    print row['rec_id']
    for col in ['ingred_text','proced_text','html_title','rec_name']:
        #print row[col]
        newrow[col] = html2utf8(row[col].decode('utf-8'))
                 
    cursor.execute("""update fixcopy set ingred_text = %s,
                                         proced_text = %s,
                                         html_title = %s,
                                         rec_name = %s
                      where rec_id = %s""",
                   (newrow['ingred_text'],newrow['proced_text'],
                    newrow['html_title'],newrow['rec_name'],
                    row['rec_id']))
db.commit()

cursor.close()


