#!/usr/bin/python

import sys
import os
import os.path
import MySQLdb
import recipe


db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="tpofofntsff",
                     db="recipesniffer-prod")

cursor = db.cursor(MySQLdb.cursors.DictCursor)


path_to_recipes_list = [ '/home/amorten/RecipeFiles/Sites/FoodDownUnder.com/Recipes']
tablename = "testing2"


for recipe_path in path_to_recipes_list:
    
    sys.path.insert(0,recipe_path)
    #print sys.path
    import recipe_parser as recp

    file_list = os.listdir(recipe_path)

    counter = 1
    for f in file_list:
        counter += 1

        #print f

        fullfilename = recipe_path+r"/"+f
        infile = open(fullfilename,"r")
        text = infile.read()
        infile.close()

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

        if (ingred_text and proced_text and
            url_domain and url_remainder and
            html_title and rec_name and
            date_update and date_original):
            
            cursor.executemany("INSERT INTO " +tablename+" "+"""
                           (ingred_text,proced_text,
                            url_domain,url_remainder,
                            html_title,rec_name,
                            date_update,date_original,
                            file_dir,file_name)
                           VALUES
                           (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                           """,
                           [(ingred_text,proced_text,
                             url_domain,url_remainder,
                             html_title,rec_name,
                             date_update,date_original,
                             file_dir,file_name)]
                           )
        else:
            if rec_name:
                print f
            
        #if counter == 10:
        #    break

        if counter % 1000 == 0:
            db.commit()
            

    db.commit() 


cursor.close()
