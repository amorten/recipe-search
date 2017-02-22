#!/usr/bin/python

import sys
import os
import os.path
import MySQLdb
from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="pwd4recDB",
                     db="recipes")

cursor = db.cursor(MySQLdb.cursors.DictCursor)


path_to_parser = '~/Projects/RecipeSearch/RecipeFiles/Sites/AllRecipes.com'
path_to_recipes_list = [ '~/Projects/RecipeSearch/RecipeFiles/Sites/AllRecipes.com/Temp']
tablename = "recipes"



def InsertIntoDb(datachunk,tablename):
        
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

    counter = 1
    datachunk = []
    for f in file_list:
        counter += 1

        #print f

        fullfilename = recipe_path+r"/"+f
        infile = open(fullfilename,"r")
        text = infile.read()
        infile.close()
        print f
        print 'before'
        soup = BeautifulSoup(text,convertEntities=BeautifulSoup.ALL_ENTITIES,parseOnlyThese=onlyHeadAndBody)
        print 'after'

        file_dir = recipe_path
        file_name = f
        ingred_text = recp.get_ingred_text(soup)
        proced_text = recp.get_proced_text(soup)
        url_domain = recp.get_url_domain(soup)
        url_remainder = recp.get_url_remainder(soup,f)
        html_title = recp.get_html_title(soup)
        rec_name = recp.get_rec_name(soup)
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
            print 'file_dir:\n', file_dir
            print 'file_name:\n', file_name
            print 'ingred_text:\n', ingred_text
            print 'url_domain:\n', url_domain
            print 'url_remainder:\n', url_remainder
            print 'date_update:\n', date_update
            print 'date_original:\n', date_original


        if counter % 1000 == 0:
            
            InsertIntoDb(datachunk,tablename)
            
            datachunk = []
            

    InsertIntoDb(datachunk,tablename) 


cursor.close()
