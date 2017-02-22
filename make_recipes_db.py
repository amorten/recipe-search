#!/usr/bin/python

import MySQLdb

import sys



tablename = sys.argv[1]

conn = MySQLdb.connect (host = "localhost",
                        user = "root",
                        passwd = "pwd4recDB",
                        db = "Recipes")

cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS "+tablename)
cursor.execute("""
               CREATE TABLE"""+' '+tablename+' '+"""
               (
                 rec_id  INT UNSIGNED NOT NULL AUTO_INCREMENT,
                 PRIMARY KEY (rec_id),
                 url_domain  VARCHAR(100) NOT NULL,
                 url_remainder  VARCHAR(250) NOT NULL,
                 file_dir  VARCHAR(250) NOT NULL,
                 file_name  VARCHAR(250) NOT NULL,
                 ingred_text  MEDIUMTEXT NOT NULL,
                 proced_text  MEDIUMTEXT,
                 html_title  VARCHAR(250),
                 rec_name  VARCHAR(250),
                 date_update  DATETIME NOT NULL,
                 date_original  DATETIME NOT NULL
               ) CHARACTER SET utf8
               """
               )
                 
               


# print "Hello world!"

