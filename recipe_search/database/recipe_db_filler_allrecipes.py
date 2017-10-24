#!/usr/bin/python

import datetime
import sys
import os
import os.path
import MySQLdb
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

from htmlxml2unicode import htmlxml2unicode
from htmlxmlDecoder import htmlDecoder


db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="pwd4recDB",
                     db="recipes_small",
                     use_unicode=True)

db.set_character_set('utf8')

cursor = db.cursor(MySQLdb.cursors.DictCursor)
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

path_to_parser = '/Users/amorten/Projects/RecipeSearch/RecipeFiles/Sites/AllRecipes.com/Recipes'
path_to_recipes_list = [ '/Users/amorten/Projects/RecipeSearch/RecipeFiles/Sites/AllRecipes.com/Recipes']
tablename = "recipes"
logfilename = "allrecipes_log.txt"

logfile = open(logfilename,"w")


def InsertIntoDb(datachunk,tablename):

    #for datarow in datachunk:
    #    for col in range(6):
    #        if not isinstance(datarow[col],unicode):
    #            print datarow
        
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

        #print f

        fullfilename = recipe_path+r"/"+f
        infile = open(fullfilename,"r")
        text = infile.read()
        infile.close()
        #print f
        #print 'before'
        #soup = BeautifulSoup(text,convertEntities=BeautifulSoup.ALL_ENTITIES,parseOnlyThese=onlyHeadAndBody)
        #print 'after'

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


        #if counter % 1 == 0:        
        if counter % 1000 == 0:
            
            print counter, datetime.datetime.now()
            InsertIntoDb(datachunk,tablename)
            
            datachunk = []
            

    InsertIntoDb(datachunk,tablename) 


cursor.close()
logfile.close()
