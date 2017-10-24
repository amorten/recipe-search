
#!/usr/bin/python

import MySQLdb

import sys

def create_recipes_table(cursor):

    tablename = 'Recipes'
    
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


def create_ingred_tables(cursor):

    tablename_recipes = ' Recipes '
    tablename_ingredlines = 'IngredLines'
    tablename_recingredlines = 'Recipes_IngredLines'
    tablename_ingreds = 'NaiveIngreds'
    tablename_recingred = 'Recipes_NaiveIngreds'
    tablename_ingredingredlines = 'NaiveIngreds_IngredLines'

    cursor.execute("DROP TABLE IF EXISTS "+tablename_ingredlines)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS"""+' '+tablename_ingredlines+' '+"""
                   (
                     ingred_line_id  INT UNSIGNED NOT NULL AUTO_INCREMENT,
                     PRIMARY KEY (ingred_line_id),
                     ingred_line_text VARCHAR(250) UNIQUE NOT NULL
                   ) CHARACTER SET utf8
                   """
                   )

    cursor.execute("DROP TABLE IF EXISTS "+tablename_recingredlines)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS"""+' '+tablename_recingredlines+' '+"""
                   (
                     rec_id INT UNSIGNED NOT NULL,
                     ingred_line_id  INT UNSIGNED NOT NULL,
                     PRIMARY KEY (rec_id,ingred_line_id),
                     FOREIGN KEY (rec_id) REFERENCES """+' '+tablename_recipes+' '+""" (rec_id)
                       ON DELETE CASCADE
                       ON UPDATE CASCADE,
                     FOREIGN KEY (ingred_line_id) REFERENCES"""+' '+tablename_ingredlines+' '+""" (ingred_line_id)
                       ON DELETE CASCADE
                       ON UPDATE CASCADE
                   ) CHARACTER SET utf8
                   """
                   )

    cursor.execute("DROP TABLE IF EXISTS "+tablename_ingreds)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS"""+' '+tablename_ingreds+' '+"""
                   (
                     ingred_id  INT UNSIGNED NOT NULL AUTO_INCREMENT,
                     PRIMARY KEY (ingred_id),
                     ingred_text VARCHAR(100) UNIQUE NOT NULL
                   ) CHARACTER SET utf8
                   """
                   )

    cursor.execute("DROP TABLE IF EXISTS "+tablename_ingredingredlines)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS"""+' '+tablename_ingredingredlines+' '+"""
                   (
                     ingred_id INT UNSIGNED NOT NULL,
                     ingred_line_id INT UNSIGNED NOT NULL,
                     PRIMARY KEY (ingred_id,ingred_line_id),
                     FOREIGN KEY (ingred_id) REFERENCES """+' '+tablename_ingreds+' '+"""(ingred_id)
                       ON DELETE CASCADE
                       ON UPDATE CASCADE,
                     FOREIGN KEY (ingred_line_id) REFERENCES"""+' '+tablename_ingredlines+' '+"""(ingred_line_id)
                       ON DELETE CASCADE
                       ON UPDATE CASCADE
                   ) CHARACTER SET utf8
                   """
                   )

    cursor.execute("DROP TABLE IF EXISTS "+tablename_recingred)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS"""+' '+tablename_recingred+' '+"""
                   (
                     rec_id INT UNSIGNED NOT NULL,
                     ingred_id INT UNSIGNED NOT NULL,
                     PRIMARY KEY (rec_id,ingred_id),
                     FOREIGN KEY (rec_id) REFERENCES """+' '+tablename_recipes+' '+"""(rec_id)
                       ON DELETE CASCADE
                       ON UPDATE CASCADE,
                     FOREIGN KEY (ingred_id) REFERENCES"""+' '+tablename_ingreds+' '+"""(ingred_id)
                       ON DELETE CASCADE
                       ON UPDATE CASCADE
                   ) CHARACTER SET utf8
                   """
                   )
