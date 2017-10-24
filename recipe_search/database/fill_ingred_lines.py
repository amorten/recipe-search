
import MySQLdb
import re
import datetime


print 'Begin File',datetime.datetime.now()


tb_recipes = ' Recipes '
tb_ingredlines = ' IngredLines '
tb_recingredlines = ' Recipes_IngredLines '
tb_ingreds = ' NaiveIngreds '
tb_recingreds = ' Recipes_NaiveIngreds '
tb_ingredingredlines = ' NaiveIngreds_IngredLines '



db = MySQLdb.connect (host = "localhost",
                        user = "root",
                        passwd = "pwd4recDB",
                        db = "recipes_small")

db.set_character_set('utf8')
cursor = db.cursor(MySQLdb.cursors.DictCursor)
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')


print "Executing select statement",datetime.datetime.now()
cursor.execute ("""select rec_id,ingred_text 
                   from"""+' '+tb_recipes)
print "Fetching",datetime.datetime.now()
recipe_rows = cursor.fetchall()
#cursor.close()

counter = 0
#ingred_lines = []
#rec_ingred_lines = []
#ingreds = []

print 'Beginning loop',datetime.datetime.now()
for recipe in recipe_rows:
    
    counter += 1

    rec_id = recipe['rec_id']


    for line in recipe['ingred_text'].splitlines():
        
        

        ingred_line = line
        #print "ingred_line:", ingred_line
        
        cursor.execute("SELECT ingred_line_id FROM"+
                       tb_ingredlines+"WHERE ingred_line_text = %s",
                       (ingred_line,))
        dictresult = cursor.fetchone()
        if dictresult:
            ingred_line_id = dictresult['ingred_line_id']
        else:
            cursor.execute("INSERT IGNORE INTO"+tb_ingredlines+
                           "(ingred_line_text) VALUES"+
                           "(%s)",(ingred_line,))
            cursor.execute("SELECT LAST_INSERT_ID() AS lastid")
            ingred_line_id = cursor.fetchone()['lastid']


        cursor.execute("INSERT IGNORE INTO"+tb_recingredlines+
                       "(rec_id,ingred_line_id) VALUES "+
                       "(%s,%s)",(rec_id,ingred_line_id))
 
        #print line
        regexp = re.compile(r'\W+',re.UNICODE) #removes non-alphanumeric
        line = regexp.sub(' ',line)
        #print line
        regexp = re.compile(r'\d+',re.UNICODE) #removes numbers
        line = regexp.sub(' ',line)
        #print line
        regexp = re.compile(r'\s.\s',re.UNICODE) #removes single char words
        line = regexp.sub(' ',line)
        #print line
        
        #print line.split()

        for word in line.split():

            cursor.execute("SELECT ingred_id FROM"+
                           tb_ingreds+"WHERE ingred_text = %s",
                           (word,))
            dictresult = cursor.fetchone()
            if dictresult:
                ingred_id = dictresult['ingred_id']
            else:
                cursor.execute("INSERT IGNORE INTO"+tb_ingreds+
                               "(ingred_text) VALUES "+
                               "(%s)",(word,))
            
                cursor.execute("SELECT LAST_INSERT_ID() AS lastid")
                ingred_id = cursor.fetchone()['lastid']

            #print word, ingred_id
            cursor.execute("INSERT IGNORE INTO"+tb_ingredingredlines+
                           "(ingred_id,ingred_line_id) VALUES"+
                           "(%s,%s)",(ingred_id,ingred_line_id))
            cursor.execute("INSERT IGNORE INTO"+tb_recingreds+
                           "(rec_id,ingred_id) VALUES"+
                           "(%s,%s)",(rec_id,ingred_id))
 

    

    if counter < 10000:
        if counter % 1000 == 0:
            print counter, datetime.datetime.now()
    elif counter % 10000 == 0:
        print counter, datetime.datetime.now()
        db.commit()
        
        #if counter == 500:
         #   break
#print ingred_line
#print ingreds


cursor.close()

db.commit()

print "Finished",datetime.datetime.now()
