#!/usr/bin/python

from . import get_db,get_cursor

import datetime
import sys
import os
import os.path
import MySQLdb
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

from htmlxml2unicode import htmlxml2unicode
from htmlxmlDecoder import htmlDecoder



def fill_recipe_table(db, cursor,
                      path_to_recipes_list, path_to_parser,
                      logfile_name):
    

    tablename='Recipes'
    logfile = open(logfile_name,"w")

    def insert_multiple_recipes(datachunk,tablename):

        cursor.executemany("INSERT INTO " +tablename+" "+"""
                               (ingred_text,proced_text,
                                url_domain,url_remainder,
                                html_title,rec_name,
                                date_update,date_original,
                                file_dir,file_name)
                               VALUES
                               (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                               """,
                           datachunk)
        db.commit()
        return None

    onlyHeadAndBody = SoupStrainer(['head','body'])

    for recipe_path in path_to_recipes_list:

        sys.path.insert(0,recipe_path)
        sys.path.insert(0,path_to_parser)
        #print sys.path
        import recipe_parser as recp

        file_list = os.listdir(recipe_path)

        counter = 0
        print counter, datetime.datetime.now()
        datachunk = []
        for f in file_list:
            counter += 1

            fullfilename = recipe_path+r"/"+f
            infile = open(fullfilename,"r")
            text = infile.read()
            infile.close()
            #soup = BeautifulSoup(text,convertEntities=BeautifulSoup.ALL_ENTITIES,parseOnlyThese=onlyHeadAndBody)

            text = htmlDecoder(text)[0]
            text = htmlxml2unicode(text)

            file_dir = recipe_path
            file_name = f
            ingred_text = recp.get_ingred_text(text)
            proced_text = recp.get_proced_text(text)
            url_domain = recp.get_url_domain(text)
            url_remainder = recp.get_url_remainder(text,f)
            html_title = recp.get_html_title(text)
            rec_name = recp.get_rec_name(text)
            date_update = recp.get_date_update(fullfilename)
            date_original = recp.get_date_original(fullfilename)


            if (ingred_text and
                url_domain and url_remainder and
                date_update and date_original):

                datachunk.append((ingred_text,proced_text,
                                 url_domain,url_remainder,
                                 html_title,rec_name,
                                 date_update,date_original,
                                 file_dir,file_name))
            else:
                print >>logfile, 'file_dir:\n', file_dir
                print >>logfile, 'file_name:\n', file_name
                print >>logfile, 'ingred_text:\n', ingred_text
                print >>logfile, 'url_domain:\n', url_domain
                print >>logfile, 'url_remainder:\n', url_remainder
                print >>logfile, 'date_update:\n', date_update
                print >>logfile, 'date_original:\n', date_original


            if counter % 1000 == 0:

                print counter, datetime.datetime.now()
                insert_multiple_recipes(datachunk,tablename)

                datachunk = []


        insert_multiple_recipes(datachunk,tablename) 


    cursor.close()
    logfile.close()
